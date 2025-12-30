import argparse
import logging

from aiohttp import web

from dogtraining.server.training_database import TrainingDatabase
from dogtraining.server.training_handler import (
    TrainingHandler,
    cors_handler,
    user_authentication,
)

parser = argparse.ArgumentParser(prog="Dogtraining Server")
parser.add_argument(
    "--host",
    default="localhost",
    type=str,
)
parser.add_argument(
    "--frontend_host_url",
    default="http://localhost:5173",
    type=str,
)
parser.add_argument("--port", default=5000, type=int)
parser.add_argument(
    "--connection",
    default=None,
    type=str,
)

_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = parser.parse_args()
    app = web.Application(
        middlewares=[
            cors_handler,
            user_authentication,
        ]
    )
    app["frontend_host_url"] = args.frontend_host_url
    async def init_db(app):
        _logger.info("Start Initializing Database")
        training_database = TrainingDatabase(connection=args.connection)
        _logger.info("Finished Initializing Database")
        _logger.info("Start Initializing Routes")
        training_handler = TrainingHandler(training_database=training_database)
        app.add_routes(
            [
                web.get("/trainings", training_handler.get_all_trainings),
                web.get("/trainings/{id}", training_handler.get_training_by_id),
                web.get("/cards", training_handler.get_all_cards),
                web.get("/cards/{id}", training_handler.get_card_by_id),
                web.post("/cards", training_handler.create_card_entry),
                web.post("/trainings", training_handler.create_training_entry),
                web.get("/training_types", training_handler.get_all_training_types),
                web.post("/dogs", training_handler.create_dog_entry),
                web.get("/dogs", training_handler.get_all_dogs),
                web.get("/dogs/{id}", training_handler.get_dog_by_id),
            ]
        )
        _logger.info("Finished Initializing Routes")
        yield

    app.cleanup_ctx.append(init_db)
    web.run_app(
        app=app,
        host=args.host,
        port=args.port,
    )
