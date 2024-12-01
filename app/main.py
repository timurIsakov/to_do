from fastapi import FastAPI

from app.routers.task import task_router
from app.routers.user import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(task_router)


@app.get("/")
def index():
    return {"status": 200}
