
import argparse
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import sql
from server.models import Base


parser = argparse.ArgumentParser(prog='Dogtraining Server')
parser.add_argument(
    "--schema_name",
    default=None,
    type=str,
)
parser.add_argument(
    "--db_type",
    default="sqlite",
    type=str
)
parser.add_argument(
    "--connection",
    required=True,
    type=str,
)
if __name__ == "__main__":
    args = parser.parse_args()

    async def init_db(*, connection, db_type=None, schema_name=None):
        engine = create_async_engine(connection)
        async with engine.begin() as conn:

            if db_type == "postgres":
                await conn.execute(sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))

            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_db(connection=args.connection, db_type=args.db_type, schema_name=args.schema_name))
