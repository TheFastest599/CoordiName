# main.py
import uvicorn
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    is_dev = os.getenv("DEV_MODE") == "true"
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "app:app",  # Pass the app as an import string
        host="127.0.0.1" if is_dev else "0.0.0.0",
        port=port,
        reload=is_dev,
        workers=1 if is_dev else (os.cpu_count() * 2 + 1)
    )
