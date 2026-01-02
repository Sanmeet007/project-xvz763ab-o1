import dotenv, os

dotenv.load_dotenv(".env")
dotenv.load_dotenv(".env.local")

from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base
from app.api.routes import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="DocWise API")

app.include_router(auth.router)
