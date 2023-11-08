import uuid
from os.path import join, dirname

from app.db.database import engine
from app.db.models import Base, DifficultyLevel, Role

# file = join(dirname(__file__), "pic.jpg")
# file = join(dirname(__file__), "kitty.jpg")
# pic = open(file, "rb").read()

MODEL_IDS = {"user_id": uuid.uuid4(), "task_id": uuid.uuid4()}

INITIAL_DATA = {
    # "profile_images": [
    #     {
    #         "name": "Nemo",
    #         "content": pic,
    #     },
    # ],
    ##########
    "users": [
        {
            "id": MODEL_IDS["user_id"],
            "full_name": "Pandu",
            "nickname": "Djangolo",
            "email": "djangolo@mail.com",
            "about": "Happy coder",
            "task_stars_received": 0,
            "solution_stars_received": 0,
            "role": Role.user,
        },
    ],
    "tasks": [
        {
            "id": MODEL_IDS["task_id"],
            "name": "Add two numbers",
            "difficulty_level": DifficultyLevel.easy,
            "author_id": MODEL_IDS["user_id"],
        }
    ],
    # "solutions": [],
    # "task_descriptions": [],
    # "solution_descriptions": [],
    # "task_description_images": [],
    # "solution_description_images": [],
    # "profile_images": [],
    # "test_data": [],
    # "test_cases": [],
    # "tags": [],
    # "tasks_tags": [],
    # "hints": [],
    # "task_votes": [],
    # "solution_votes": [],
}


async def initialize_table(target, target_name, connection):
    connection.execute(target.insert(), INITIAL_DATA[target_name])
    connection.commit()


async def initialize_database():
    connection = engine.connect()
    table_models = {cls.__tablename__: cls.__table__ for cls in Base.__subclasses__()}
    for table_name in INITIAL_DATA:
        model = table_models[table_name]
        await initialize_table(model, table_name, connection)
