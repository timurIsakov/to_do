from fastapi import APIRouter
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session, selectinload
from starlette import status
from starlette.responses import Response

from app.data_source.config import engine
from app.data_source.models import User
from app.schemas.user import UserCreateSchema, UserReadSchema, UserDetailsReadSchema

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateSchema):
    with Session(bind=engine) as session:
        session.execute(insert(User).values(**user.model_dump()))
        session.commit()


@user_router.get("/", response_model=list[UserReadSchema])
def get_users():
    with Session(bind=engine) as session:
        users = session.execute(select(User)).scalars().all()
    return users


@user_router.get("/{user_id}", response_model=UserDetailsReadSchema)
def get_details_user(user_id: int):
    with Session(bind=engine) as session:
        user = session.execute(
            select(User).where(User.id == user_id).options(selectinload(User.tasks))).scalars().first()
        if user is None:
            return Response(status_code=404)
    return user


@user_router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int, user: UserCreateSchema):
    with Session(bind=engine) as session:
        response = session.execute(update(User).where(User.id == user_id).values(**user.model_dump()))
        if response.rowcount == 0:
            return Response(status_code=404)
        else:
            session.commit()


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    with Session(bind=engine) as session:
        response = session.execute(delete(User).where(User.id == user_id))
        if response.rowcount == 0:
            return Response(status_code=404)
        else:
            session.commit()
