from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers  import posts, users, auth, votes

# models.Base.metadata.create_all(bind = engine) # only purpose is to create the tables if they don't exist

app = FastAPI()

origins = ["*"] # any domain can hit the api

app.add_middleware(
    CORSMiddleware, #middleware is like a function that runs before every request 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Hello from Post Votes API version-0.1"}