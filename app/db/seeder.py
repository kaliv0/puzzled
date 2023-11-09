from uuid import uuid4
from os.path import join, dirname

from app.db.database import engine
from app.db.models import Base, DifficultyLevel, Role

db_resources_path = join(dirname(__file__), "resources")
addition_example_path = join(db_resources_path, "addition_example.gif")
addition_example_img = open(addition_example_path, "rb").read()
addition_solution_path = join(db_resources_path, "addition_solution.png")
addition_solution_img = open(addition_solution_path, "rb").read()
avatar_path = join(db_resources_path, "profile_image.jpg")
avatar_img = open(avatar_path, "rb").read()


SOLUTION_CONTENT = """
def add_nums(a: int, b: int) -> int:
    return a + b
"""

MODEL_IDS = {
    "user_id": uuid4(),
    "task_id": uuid4(),
    "solution_id": uuid4(),
    "task_description_id": uuid4(),
    "solution_description_id": uuid4(),
    "task_description_image_id": uuid4(),
    "solution_description_image_id": uuid4(),
    "profile_image_id": uuid4(),
}

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
            "full_name": "Kumar Pandu",
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
    "solutions": [
        {
            "id": MODEL_IDS["solution_id"],
            "name": "200 % faster implementation",  # TODO: remove property?
            "task_id": MODEL_IDS["task_id"],
            "author_id": MODEL_IDS["user_id"],
            "description": "Simply use + operator",
            "content": SOLUTION_CONTENT,
            "votes": 0,
        }
    ],
    "task_descriptions": [
        {
            "id": MODEL_IDS["task_description_id"],
            "task_id": MODEL_IDS["task_id"],
            "text": "Write a function that adds given arguments together",
            "links": [
                "https://en.wikipedia.org/wiki/Addition",
                "https://math.fandom.com/wiki/Addition",
            ],
        },
    ],
    "solution_descriptions": [
        {
            "id": MODEL_IDS["solution_description_id"],
            "solution_id": MODEL_IDS["solution_id"],
            "text": "Simply use the plus (+) sign",
        },
    ],
    "task_description_images": [
        {
            "id": MODEL_IDS["task_description_image_id"],
            "task_description_id": MODEL_IDS["task_description_id"],
            "name": "Addition example",  # TODO: remove?
            "content": addition_example_img,
        }
    ],
    "solution_description_images": [
        {
            "id": MODEL_IDS["solution_description_image_id"],
            "solution_description_id": MODEL_IDS["solution_description_id"],
            "name": "Addition example",  # TODO: remove?
            "content": addition_solution_img,
        }
    ],
    "profile_images": [
        {
            "id": MODEL_IDS["profile_image_id"],
            "user_id": MODEL_IDS["user_id"],
            "name": "Addition example",  # TODO: remove?
            "content": avatar_img,
        }
    ],
    # "test_data": [],
    # "test_cases": [],
    # "tags": [],
    # "tasks_tags": [],
    # "hints": [],
    # "task_votes": [],
    # "solution_votes": [],
}


async def initialize_table(target, target_data, connection):
    connection.execute(target.insert(), target_data)
    connection.commit()


async def initialize_database():
    connection = engine.connect()
    table_models = {cls.__tablename__: cls.__table__ for cls in Base.__subclasses__()}
    for table_name, table_data in INITIAL_DATA.items():
        model = table_models[table_name]
        await initialize_table(model, table_data, connection)
