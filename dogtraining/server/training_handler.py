from aiohttp import web

from dogtraining.server.training_database import (
    CardFull,
    CardNotFound,
    CardSpec,
    DatabaseException,
    DogSpec,
    DogSpecInvalid,
    InvalidPayload,
    TrainingDatabase,
    TrainingSpec,
    TrainingType,
)


@web.middleware
async def user_authentication(request, handler):
    user_id = request.headers.get("user_id")
    if not user_id:
        return web.json_response(
            status=401,
            data={
                "error": "Unauthorized access, provide the correct authorization header."
            },
        )
    resp = await handler(request)
    return resp


@web.middleware
async def cors_handler(request: web.Request, handler):
    cors_headers = {
        "Access-Control-Allow-Origin": request.app["frontend_host_url"],
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,user_id",
    }
    cors_handler = {
        "Access-Control-Allow-Origin": request.app["frontend_host_url"],  # or specific origin
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400",
    }

    if request.method == "OPTIONS":
        return web.Response(status=204, headers=cors_headers)

    response = await handler(request)

    for key, value in cors_headers.items():
        response.headers[key] = value

    return response


class TrainingHandler:
    def __init__(self, *, training_database):
        self._training_database: TrainingDatabase = training_database

    async def get_all_trainings(self, request: web.Request):
        return web.json_response(
            data=[
                training.as_dict()
                for training in await self._training_database.get_all_training_entries(
                    user_id=request.headers.get("user_id"),
                )
            ]
        )

    async def get_training_by_id(self, request: web.Request):
        training_id = request.match_info["id"]
        try:
            training = await self._training_database.get_training_entry_by_id(
                training_id=training_id, user_id=request.headers.get("user_id")
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
        cards = await self._training_database.get_all_card_entries(
            user_id=request.headers.get("user_id"),
        )
        return web.json_response(data=[card.as_dict() for card in cards])

    async def get_card_by_id(self, request: web.Request):
        card_id = request.match_info["id"]
        try:
            card = await self._training_database.get_card_entry_by_id(
                card_id=card_id,
                user_id=request.headers.get("user_id"),
            )
            return web.json_response(data=card.as_dict())
        except DatabaseException as e:
            return web.json_response(status=400, data={"error": str(e)})

    async def create_card_entry(self, request: web.Request):
        try:
            card_spec = CardSpec.from_json(
                data=await request.json(), user_id=request.headers.get("user_id")
            )
            card = await self._training_database.create_card_entry(card_spec=card_spec)
            return web.json_response(data=card.as_dict())
        except InvalidPayload as e:
            return web.json_response(
                status=400,
                data={"error": str(e)},
            )

    async def create_training_entry(self, request: web.Request):
        try:
            training_spec = TrainingSpec.from_json(
                data=await request.json(), user_id=request.headers.get("user_id")
            )
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

    async def get_all_training_types(self, request: web.Request):
        return web.json_response(data=[type.value for type in TrainingType])

    async def create_dog_entry(self, request: web.Request):
        try:
            dog_spec = DogSpec.from_json(
                data=await request.json(), user_id=request.headers.get("user_id")
            )
            dog = await self._training_database.create_dog_entry(
                dog_spec=dog_spec,
            )
            return web.json_response(data=dog.as_dict())
        except (InvalidPayload, DogSpecInvalid) as e:
            return web.json_response(
                status=400,
                data={
                    "error": str(e),
                },
            )

    async def get_dog_by_id(self, request: web.Request):
        dog_id = request.match_info["id"]
        try:
            dog = await self._training_database.get_dog_by_id(
                dog_id=dog_id,
                user_id=request.headers.get("user_id"),
            )
            return web.json_response(data=dog.as_dict())
        except DatabaseException as e:
            return web.json_response(status=400, data={"error": str(e)})

    async def get_all_dogs(self, request: web.Request):
        dogs = await self._training_database.get_all_dogs(
            user_id=request.headers.get("user_id")
        )
        return web.json_response(data=[dog.as_dict() for dog in dogs])
