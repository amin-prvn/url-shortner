from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import declarative_base, sessionmaker
from asyncio import current_task

from app.api.config import get_settings


Base = declarative_base()

class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
    
    def __getattr__(self, name):
        return getattr(self._session, name)
    
    def init(self):
        self._engine = create_async_engine(
            get_settings().DB_CONFIG,
            future=True,
            echo=True,
        )
        session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
        self._session = async_scoped_session(session, scopefunc=current_task)

    
    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

db=AsyncDatabaseSession()