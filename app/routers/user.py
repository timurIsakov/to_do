from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session, selectinload
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from app.data_source.config import get_db_session
from app.data_source.models import User
from app.schemas.user import UserCreateSchema, UserReadSchema, UserDetailsReadSchema

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=UserReadSchema)
def create_user(user: UserCreateSchema, session: Annotated[Session, Depends(get_db_session)]):
    response = session.execute(insert(User).values(**user.model_dump()).returning(User)).scalar_one()
    session.commit()
    return response


@user_router.get("/", response_model=list[UserReadSchema])
def get_users(session: Annotated[Session, Depends(get_db_session)]):
    users = session.execute(select(User)).scalars().all()
    return users


@user_router.get("/{user_id}", response_model=UserDetailsReadSchema)
def get_details_user(user_id: int, session: Annotated[Session, Depends(get_db_session)]):
    user = session.execute(
        select(User).where(User.id == user_id).options(selectinload(User.tasks))
    ).scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@user_router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int, user: UserCreateSchema, session: Annotated[Session, Depends(get_db_session)]):
    response = session.execute(
        update(User).where(User.id == user_id).values(**user.model_dump()))
    if response.rowcount == 0:
        return Response(status_code=404)
    else:
        session.commit()


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Annotated[Session, Depends(get_db_session)]):
    response = session.execute(delete(User).where(User.id == user_id))
    if response.rowcount == 0:
        return Response(status_code=404)
    else:
        session.commit()
