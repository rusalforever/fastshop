import logging

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.base_settings import base_settings


logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self):
        self._engine = None
        self._session = None

    def connect(self):
        logger.info("Connecting to the PostgreSQL database.")
        self._engine = create_async_engine(
            url=base_settings.postgres.url,
            echo=True,
        )
        self._session = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
        )
        logger.info("Successfully connected to the PostgreSQL database.")

    async def disconnect(self):
        if self._engine:
            await self._engine.dispose()
            logger.info("Disconnected from the PostgreSQL database.")

    def get_engine(self):
        if not self._engine:
            raise RuntimeError("Engine not initialized. Call 'connect()' first.")
        return self._engine

    async def get_db(self):
        if not self._session:
            raise RuntimeError("Session not initialized. Call 'connect()' first.")
        async with self._session() as session:
            yield session


postgres = Database()


async def get_session():
    async for session in postgres.get_db():
        yield session
