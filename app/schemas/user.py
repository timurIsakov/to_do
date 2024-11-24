from pydantic import BaseModel
from task import Task


class User(BaseModel):
    name: str
    tasks: list[Task]
