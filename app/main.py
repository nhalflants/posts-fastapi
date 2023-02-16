from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models as models
import app.database as db
import app.config
from app.routers import post, user, authentication, vote

# Command to create sqlachemy tables upon app startup
# models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)