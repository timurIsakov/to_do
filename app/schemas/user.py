from pydantic import BaseModel, ConfigDict

from app.schemas.task import TaskReadSchemas


class UserBaseSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserReadSchema(UserBaseSchema):
    id: int


class UserDetailsReadSchema(UserBaseSchema):
    id: int
    tasks: list[TaskReadSchemas]


class UserCreateSchema(UserBaseSchema):
    pass
