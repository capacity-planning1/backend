from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import create_db_and_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title='Capacity Planning API',
    version='1.0.0',
    lifespan=lifespan,
)


@app.get('/')
def read_root():
    return {'message': 'Capacity Planning API is running'}
