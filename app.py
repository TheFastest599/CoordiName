from fastapi import FastAPI
from routes.auth import authRouter
from routes.client import clientRouter
from routes.api import apiRouter, sheduler
from fastapi.middleware.cors import CORSMiddleware
from config.database import ping_mongodb, close_mongodb
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await ping_mongodb()
    sheduler.start()
    yield
    # Shutdown
    await close_mongodb()

origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:5000",  # FastAPI server (if accessed directly)
    # Add more origins as needed
]

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["auth-token", "api-key"],  # Allow certain headers
    # Explicitly allow auth token and API key headers
    expose_headers=["auth-token", "api-key"],
)


app.include_router(authRouter)
app.include_router(clientRouter)
app.include_router(apiRouter)
