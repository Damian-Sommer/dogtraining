from aiohttp import web

from dogtraining.server.training_database import (
    CardFull,
    CardNotFound,
    CardSpec,
    DatabaseException,
    InvalidPayload,
    TrainingDatabase,
    TrainingSpec,
)


class TrainingHandler:
    def __init__(self, *, training_database):
        self._training_database: TrainingDatabase = training_database

    async def get_all_trainings(self, request: web.Request):
        return web.json_response(
            data=[
                training.as_dict()
                for training in await self._training_database.get_all_training_entries()
            ]
        )

    async def get_training_by_id(self, request: web.Request):
        training_id = request.match_info["id"]
        try:
            training = await self._training_database.get_training_entry_by_id(
                training_id=training_id
            )
            return web.json_response(data=training.as_dict())
        except DatabaseException as e:
            return web.json_response(
                status=400,
                data={
                    "error": str(e),
                },
            )

    async def get_all_cards(self, request: web.Request):
        cards = await self._training_database.get_all_card_entries()
        return web.json_response(data=[card.as_dict() for card in cards])

    async def get_card_by_id(self, request: web.Request):
        card_id = request.match_info["id"]
        try:
            card = await self._training_database.get_card_entry_by_id(card_id=card_id)
            return web.json_response(data=card.as_dict())
        except DatabaseException as e:
            return web.json_response(status=400, data={"error": str(e)})

    async def create_card_entry(self, request: web.Request):
        try:
            card_spec = CardSpec.from_json(data=await request.json())
            card = await self._training_database.create_card_entry(card_spec=card_spec)
            return web.json_response(data=card.as_dict())
        except InvalidPayload as e:
            return web.json_response(
                status=400,
                data={"error": str(e)},
            )

    async def create_training_entry(self, request: web.Request):
        try:
            training_spec = TrainingSpec.from_json(data=await request.json())
            trainings = await self._training_database.create_training_entry(
                training_spec=training_spec
            )
            return web.json_response(
                data=[training.as_dict() for training in trainings]
            )
        except (InvalidPayload, CardNotFound, CardFull) as e:
            return web.json_response(
                status=400,
                data={
                    "error": str(e),
                },
            )
