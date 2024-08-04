from fastapi import HTTPException,  Depends
from fastapi.security.api_key import APIKeyHeader
from config.database import collection_user, collection_apiKey
from bson import ObjectId
import os
from dotenv import load_dotenv
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


load_dotenv()

# Secret key and algorithm
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

# Setup API key header dependency
header_apiKey = APIKeyHeader(name="api-key", auto_error=True)
header_authToken = APIKeyHeader(name="auth-token", auto_error=True)


# Get Api key details
async def get_api_key(apiKey: str = Depends(header_apiKey)):
    if len(apiKey) == 0:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    apiKeyDetails = await collection_apiKey.find_one({"key": apiKey})
    if not apiKeyDetails:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return apiKeyDetails


# Verify auth token and return user
async def get_auth_token(authToken: str = Depends(header_authToken)):
    try:
        token = jwt.decode(authToken, SECRET_KEY, algorithms=[ALGORITHM])
        user = await collection_user.find_one({"_id": ObjectId(token["id"])})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid Auth Token")
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
