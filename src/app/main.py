from fastapi import FastAPI

from app.database import db


def init_app():
    db.init()
    app = FastAPI(
        title="Url Shortner App",
        description="Make Url shorter and give secret-key to Man/Woman who short the url for seeing number of clicks and deleting option.",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()
    
    from app.api.views import api
    
    app.include_router(
        api,
        prefix="/api/v1",
    )
    return app


app = init_app()