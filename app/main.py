
import dotenv, os

dotenv.load_dotenv(".env")
dotenv.load_dotenv(".env.local")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.database import engine
from app.db.models import Base
from app.api.routes import auth
from app.api.routes import password, user  # NEW

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DocWise API")

app.include_router(auth.router)
app.include_router(password.router)  # /api/forgot-password*, etc.
app.include_router(user.router)      # /api/user/*

# Serve uploaded profile images
if not os.path.exists("media"):
    os.makedirs("media")

app.mount("/media", StaticFiles(directory="media"), name="media")