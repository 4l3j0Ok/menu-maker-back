from fastapi import FastAPI, responses
import uvicorn
import importlib
from modules import config


app = FastAPI()
for module in config.ROUTERS:
    router = importlib.import_module(f"routers.{module}")
    app.include_router(
        router=router.router,
        prefix=f"/{module}",
        tags=[module.capitalize()]
        )


@app.get("/", tags=["Main"])
async def home() -> responses.RedirectResponse:
    "Página de inicio. Redirecciona a la documentación."
    return responses.RedirectResponse(app.docs_url)


@app.get("/alive", tags=["Main"])
async def alive() -> str:
    "Chequea si la aplicación está viva."
    return "Estoy vivo!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
