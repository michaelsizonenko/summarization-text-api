import uvicorn as uvicorn
from databases import Database
from fastapi import FastAPI

from starlette.routing import Mount

from config import system_config
from app.routers import document

app = FastAPI(title="Summarization Text Api")
database = Database(url=system_config.db_async_url)

app.include_router(document.router, prefix='/document')


def inject_db(app: FastAPI, db: Database):
    app.state.db = db
    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.state.db = db


@app.on_event("startup")
async def startup():
    await database.connect()
    inject_db(app, database)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == '__main__':
    uvicorn.run("main:app", **system_config.fast_api_config)

