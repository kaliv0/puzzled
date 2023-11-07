from os.path import join, dirname

from app.db.database import engine
from app.db.models import Base

# file = join(dirname(__file__), "pic.jpg")
# file = join(dirname(__file__), "kitty.jpg")
# pic = open(file, "rb").read()


INITIAL_DATA = {
    # "profile_images": [
    #     {
    #         "name": "Nemo",
    #         "content": pic,
    #     },
    # ],
    ##########
    "users": [],
    "tasks": [],
    "solutions": [],
    "task_descriptions": [],
    "solution_descriptions": [],
    "task_description_images": [],
    "solution_description_images": [],
    "profile_images": [],
    "test_data": [],
    "test_cases": [],
    "tags": [],
    "tasks_tags": [],
    "hints": [],
    "task_votes": [],
    "solution_votes": [],
}


async def initialize_table(target, connection):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        # TODO: migrate to async
        connection.execute(target.insert(), INITIAL_DATA[tablename])
    connection.commit()


async def initialize_database():
    table_models = [cls.__table__ for cls in Base.__subclasses__()]
    for model in table_models:
        # TODO: move engine.connect inside initialize_table?
        await initialize_table(model, engine.connect())
