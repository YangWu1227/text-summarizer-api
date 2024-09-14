import os 
import logging

from fastapi import FastAPI 
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, run_async 

logger = logging.getLogger('uvicorn')

# Define the aerich.models
TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}

def init_db(app: FastAPI) -> None:

    # Registers Tortoise-ORM with set-up and tear-down inside a FastAPI application’s lifespan
    register_tortoise(
        app=app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        # Do not generate schema immediately for production
        generate_schemas=False,
        # True to add some automatic exception handlers for DoesNotExist & IntegrityError, not recommended for production
        add_exception_handlers=True,
    )

async def generate_schema() -> None:
    logger.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.tortoise"]},
    )
    logger.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()

if __name__ == '__main__':

    run_async(generate_schema())
