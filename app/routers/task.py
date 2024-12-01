from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Body
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app.data_source.config import engine, get_db_session
from app.data_source.models import Task
from app.schemas.task import TaskBaseSchemas, TaskReadSchemas

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(user_id: Annotated[int, Body()], task: TaskBaseSchemas,
                session: Annotated[Session, Depends(get_db_session)]):
    session.execute(insert(Task).values(**task.model_dump(), user_id=user_id))
    session.commit()


@task_router.get("/", response_model=list[TaskReadSchemas])
def get_tasks(user_id: Annotated[int, Body()]):
    with Session(bind=engine) as session:
        tasks = session.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
        if tasks is None:
            return Response(status_code=404)
    return tasks


@task_router.get("/{user_id}/{task_id}", response_model=TaskReadSchemas)
def get_task(user_id: int, task_id):
    with Session(bind=engine) as session:
        task = session.execute(select(Task).where(Task.user_id == user_id and Task.id == task_id)).scalar()
        if task is None:
            return Response(status_code=404)
    return task


@task_router.patch("/{user_id}/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(user_id: int, task_id: int, task: TaskBaseSchemas):
    with Session(bind=engine) as session:
        response = session.execute(
            update(Task).where(Task.user_id == user_id and Task.id == task_id).values(**task.model_dump()))
        if response.rowcount == 0:
            return Response(status_code=404)
        else:
            session.commit()


@task_router.delete("/{user_id}/{task_id}", status_code=status.HTTP_201_CREATED)
def delete_task(user_id: int, task_id: int):
    with Session(bind=engine) as session:
        response = session.execute(delete(Task).where(Task.user_id == user_id and Task.id == task_id))
        if response.rowcount == 0:
            return Response(status_code=404)
        else:
            session.commit()
