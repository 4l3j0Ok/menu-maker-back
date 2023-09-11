from fastapi import FastAPI, responses
import uvicorn
import importlib
from modules.common import config
from modules.common.logger import logger


app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION
)


for module in config.ROUTERS:
    logger.info(f"Registrando router '{module}'.")
    router = importlib.import_module(f"routers.{module}")
    app.include_router(
        router=router.router,
        prefix=f"/{module}",
        tags=[module.capitalize()]
    )


@app.get("/", tags=["Main"])
async def home() -> responses.RedirectResponse:
    "Página de inicio. Redirecciona a la documentación."
    logger.info("Redireccionando a la documentación.")
    return responses.RedirectResponse(app.docs_url)


@app.get("/alive", tags=["Main"])
async def alive() -> str:
    "Chequea si la aplicación está viva."
    return "Estoy vivo!"


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True
    )
