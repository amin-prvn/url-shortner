from sqlalchemy import Boolean, Column, Integer, String, exc
from sqlalchemy.future import select
from sqlalchemy import update

from app.api.keygen import create_unique_random_key, create_random_key
from app.database import Base, db


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    
    @classmethod
    async def create(cls, url, **kwargs):

        key = await create_unique_random_key()
        secret_key = f"{key}_{create_random_key(length=8)}"
        db_url = cls(
            target_url=url.target_url, key=key, secret_key=secret_key
        )
        db.add(db_url)       
        
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return db_url


    @classmethod
    async def get_by_key(cls, url_key: str, **kwargs):
        query = select(cls).where(cls.key == url_key, URL.is_active)
        try:
            url = await db.execute(query)
            (url,) = url.one()
        except exc.NoResultFound:
            return None
        return url


    @classmethod
    async def get_by_secret_key(cls, secret_key: str, **kwargs):
        query = select(cls).where(cls.secret_key == secret_key, URL.is_active)
        try:
            url = await db.execute(query)
            (url,) = url.one()
        except exc.NoResultFound:
            return None
        return url
    

    async def clicked(self, **kwargs):
        self.clicks += 1
        query = (
            update(URL)
            .where(URL.id == self.id)
            .values(clicks=self.clicks)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise


    async def deactive(self, **kwargs):
        query = (
            update(URL)
            .where(URL.secret_key == self.secret_key)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise