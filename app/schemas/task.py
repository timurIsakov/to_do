from pydantic import BaseModel


class TaskBaseSchemas(BaseModel):
    title: str
    description: str = ""


class TaskReadSchemas(TaskBaseSchemas):
    id: int
