from fastapi import APIRouter
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from starlette import status

from app.data_source.config import engine
from app.data_source.models import Task
from app.schemas.task import TaskBaseSchemas, TaskReadSchemas

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task: TaskBaseSchemas):
    with Session(bind=engine) as session:
        session.execute(insert(Task).values(**task.model_dump(), user_id=user_id))
        session.commit()


@task_router.get("/{user_id}", response_model=list[TaskReadSchemas])
def get_tasks(user_id: int):
    with Session(bind=engine) as session:
        tasks = session.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    return tasks


@task_router.get("/{user_id}/{task_id}", response_model=TaskReadSchemas)
def get_task(user_id: int, task_id):
    with Session(bind=engine) as session:
        task = session.execute(select(Task).where(Task.user_id == user_id and Task.id == task_id)).scalar()
    return task


@task_router.patch("/{user_id}/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(user_id: int, task_id: int, task: TaskBaseSchemas):
    with Session(bind=engine) as session:
        session.execute(update(Task).where(Task.user_id == user_id and Task.id == task_id).values(**task.model_dump()))
        session.commit()


@task_router.delete("/{user_id}/{task_id}", status_code=status.HTTP_201_CREATED)
def delete_task(user_id: int, task_id: int):
    with Session(bind=engine) as session:
        session.execute(delete(Task).where(Task.user_id == user_id and Task.id == task_id))
        session.commit()
