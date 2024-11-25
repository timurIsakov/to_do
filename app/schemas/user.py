from pydantic import BaseModel, ConfigDict

from app.schemas.task import TaskSchemas


class UserBaseSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserReadSchema(UserBaseSchema):
    id: int


class UserDetailsReadSchema(UserBaseSchema):
    id: int
    tasks: list[TaskSchemas]


class UserCreateSchema(UserBaseSchema):
    pass
