from contextlib import asynccontextmanager
from os.path import dirname, join

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.models import ProfileImage

# #### Seed DB ####

file = join(dirname(__file__), "pic.jpg")
pic = open(file, "rb").read()

INITIAL_DATA = {
    "profile_images": [
        {
            "name": "Nemo",
            "content": pic,
        },
    ],
}


async def initialize_table(target, connection):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])
    connection.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_table(ProfileImage.__table__, engine.connect())
    yield


###############

app = FastAPI(lifespan=lifespan)

# only needed if migrations are not run using alembic
# models.Base.metadata.create_all(engine)

origins = ["http://localhost:3000", "http://localhost:3001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
