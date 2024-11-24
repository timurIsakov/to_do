from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(
        url="https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_6527776a9523772f00ea671e_652778529bc67b6489d88566/scale_1200")
