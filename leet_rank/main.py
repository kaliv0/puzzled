import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from leet_rank.db import models
from leet_rank.db.database import engine

app = FastAPI()

# app.include_router(post.router)

models.Base.metadata.create_all(engine)

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
