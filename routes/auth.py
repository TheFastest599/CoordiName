from fastapi import APIRouter, Response,  HTTPException, requests, Depends
from models.users import User, LogUser, LogGoogleUser, GoogleUser
from models.apiKey import ApiKey
from config.database import collection_user, collection_apiKey
from config.middleware import get_api_key, get_auth_token
import re
import os
import bcrypt
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import secrets
import requests
from google.oauth2 import id_token
from google.auth.transport import requests


load_dotenv()


authRouter = APIRouter()

# Secret key and algorithm
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS"))


# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_google_token(payload):
    try:
        # Verify the token
        id_info = id_token.verify_oauth2_token(
            payload["credential"], requests.Request(), audience=payload["clientId"], clock_skew_in_seconds=10
        )
        # If the token is valid, return the decoded token information
        return {"message": "Token is valid", "token_info": id_info}

    except ValueError as e:
        # If the token is invalid, raise an HTTP exception
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail="Internal server error")


@authRouter.post("/auth/signup")
async def create_user(user: User, response: Response):
    try:
        user = dict(user)
        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            raise HTTPException(
                status_code=400, detail="All fields must be filled")
        if await collection_user.find_one({"email": user["email"]}):
            raise HTTPException(status_code=400, detail="User already exists")
        if len(user["password"]) < 8:
            raise HTTPException(
                status_code=400, detail="Password must be at least 8 characters long")
        if len(user["name"]) < 3:
            raise HTTPException(
                status_code=400, detail="Name must be at least 3 characters long")
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, user["email"]):
            raise HTTPException(status_code=400, detail="Invalid email format")
        # Insert user into database here
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(user["password"].encode('utf-8'), salt)
        user["password"] = hashed_password
        dateTime = datetime.now(timezone.utc)
        user["date"] = dateTime
        result = await collection_user.insert_one(user)
        data = {"id": str(result.inserted_id)}
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        auth_token = create_access_token(
            data=data, expires_delta=access_token_expires)
        new_key = secrets.token_urlsafe(32)
        apiKeyObj = {"user": data["id"], "key": new_key, "date": dateTime}
        await collection_apiKey.insert_one(dict(ApiKey(**apiKeyObj)))
        content = {"message": "User Created", "api-key": new_key, "user": {
            "name": user["name"], "email": user["email"]}}
        response.headers["auth-token"] = auth_token
        return content
    except HTTPException as e:
        logging.error(f"Unexpected error: {e}")
        # Re-raise the HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch any other unexpected exceptions
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")


# Route 2: Authenticate a user using : POST "/auht/login" . No login required
@authRouter.post("/auth/login")
async def login_user(user: LogUser, response: Response):
    try:
        user = dict(user)
        if user["email"] == "" or user["password"] == "":
            raise HTTPException(
                status_code=400, detail="All fields must be filled")
        data = await collection_user.find_one({"email": user["email"]})
        if data is None:
            raise HTTPException(status_code=400, detail="User not found!!")
        if len(user["password"]) < 8:
            raise HTTPException(
                status_code=400, detail="Password must be at least 8 characters long")
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, user["email"]):
            raise HTTPException(status_code=400, detail="Invalid email format")

        passwordCompare = bcrypt.checkpw(
            user["password"].encode('utf-8'), data["password"])
        if not passwordCompare:
            raise HTTPException(
                status_code=400, detail="Invalid Credentials!!")
        dataNew = {"id": str(data["_id"])}
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        auth_token = create_access_token(
            data=dataNew, expires_delta=access_token_expires)
        apiKey = await collection_apiKey.find_one({"user": dataNew["id"]})
        content = {"message": "User Logged In !", "api-key": apiKey["key"], "user": {
            "name": data["name"], "email": data["email"]}}
        response.headers["auth-token"] = auth_token
        return content

    except HTTPException as e:
        logging.error(f"Unexpected error: {e}")
        # Re-raise the HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch any other unexpected exceptions
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")


# Route 3: Authenticate a Google SignIn : POST "/auht/googlesignin" . No login required
@authRouter.post("/auth/google_signin")
async def login_user(user: LogGoogleUser, response: Response):
    try:
        user = dict(user)
        user = await verify_google_token(user["payload"])
        user = {
            "name": user["token_info"]["name"],
            "email": user["token_info"]["email"],
            "sub": user["token_info"]["sub"],
            "picture": user["token_info"]["picture"],
            "date": datetime.now(timezone.utc)
        }
        checkUser = await collection_user.find_one({"email": user["email"]})
        if checkUser:
            if "sub" in checkUser and checkUser["sub"] == user["sub"]:
                dataNew = {"id": str(checkUser["_id"])}
                # Update the picture if it has changed
                if user["picture"] != checkUser["picture"]:
                    await collection_user.find_one_and_update(
                        {"_id": checkUser["_id"]},
                        {"$set": {"picture": user["picture"]}}
                    )
                access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
                auth_token = create_access_token(
                    data=dataNew, expires_delta=access_token_expires)
                apiKey = await collection_apiKey.find_one({"user": dataNew["id"]})
                content = {"message": "User Logged In !", "api-key": apiKey["key"], "user": {
                    "name": checkUser["name"], "email": checkUser["email"], "picture": checkUser["picture"]}}
                response.headers["auth-token"] = auth_token
                return content
            else:
                raise HTTPException(
                    status_code=400, detail="User already exists with this email. Please login using email and password.")

        else:
            result = await collection_user.insert_one(dict(GoogleUser(**user)))
            data = {"id": str(result.inserted_id)}
            access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            auth_token = create_access_token(
                data=data, expires_delta=access_token_expires)
            new_key = secrets.token_urlsafe(32)
            apiKeyObj = {"user": data["id"],
                         "key": new_key, "date": user["date"]}
            await collection_apiKey.insert_one(dict(ApiKey(**apiKeyObj)))
            content = {"message": "User Created", "api-key": new_key, "user": {
                "name": user["name"], "email": user["email"], "picture": user["picture"]}}
            response.headers["auth-token"] = auth_token
            return content
    except HTTPException as e:
        logging.error(f"Unexpected error: {e}")
        # Re-raise the HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch any other unexpected exceptions
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")


@authRouter.post("/auth/apidetails")
async def getApiDetails(userDetails=Depends(get_auth_token), apiKeyDetails=Depends(get_api_key)):
    if str(userDetails["_id"]) != apiKeyDetails["user"]:
        raise HTTPException(
            status_code=401, detail="Invalid API Key for the user")
    res = {
        'tier': apiKeyDetails['tier'],
        'usageToday': apiKeyDetails['usageToday'],
        'usageTotal': apiKeyDetails['usageTotal']
    }
    return res
