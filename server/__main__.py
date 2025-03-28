import argparse

from aiohttp import web

from server.training_database import TrainingDatabase
from server.training_handler import TrainingHandler

parser = argparse.ArgumentParser(prog="Dogtraining Server")
parser.add_argument(
    "--host",
    default="localhost",
    type=str,
)
parser.add_argument("--port", default=5000, type=int)
parser.add_argument(
    "--connection",
    default=None,
    type=str,
)

if __name__ == "__main__":
    args = parser.parse_args()
    app = web.Application()

    async def init_db(app):
        training_database = TrainingDatabase(connection=args.connection)
        training_handler = TrainingHandler(training_database=training_database)
        app.add_routes(
            [
                web.get("/trainings", training_handler.get_all_trainings),
                web.get("/trainings/{id}", training_handler.get_training_by_id),
                web.get("/cards", training_handler.get_all_cards),
                web.get("/cards/{id}", training_handler.get_card_by_id),
                web.post("/cards", training_handler.create_card_entry),
                web.post("/trainings", training_handler.create_training_entry),
            ]
        )
        yield

    app.cleanup_ctx.append(init_db)
    web.run_app(
        app=app,
        host=args.host,
        port=args.port,
    )
