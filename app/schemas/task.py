from pydantic import BaseModel


class TaskSchemas(BaseModel):
    title: str
    description: str = ""
