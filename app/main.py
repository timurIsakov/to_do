from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.routers.task import task_router
from app.routers.user import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(task_router)


@app.get("/")
def index():
    return RedirectResponse(
        url="https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_6527776a9523772f00ea671e_652778529bc67b6489d88566/scale_1200")
