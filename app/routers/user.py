from fastapi import APIRouter
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.data_source.config import engine
from app.schemas.user import User

router = APIRouter(prefix="users")


