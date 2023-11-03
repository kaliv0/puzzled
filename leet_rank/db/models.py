import enum
from datetime import datetime
from typing import List

from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey, CheckConstraint
from sqlalchemy.sql.sqltypes import String, Integer


# TODO: move back to database.py
class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped["TaskDescription"] = relationship(
        back_populates="task",
        cascade="all, delete",
    )
    test_data: Mapped["TestData"] = relationship(
        back_populates="task", cascade="all, delete"
    )
    author_solution: Mapped["Solution"] = relationship(
        back_populates="task", cascade="all, delete"
    )
    user_solutions: Mapped[List["Solution"]] = relationship(
        back_populates="task", cascade="all, delete"
    )
    tags: Mapped["Tag"] = relationship(
        "Tag", secondary="tasks_tags", back_populates="tasks"
    )  # TODO: add cascade delete
    hints: Mapped[List["Hint"]] = relationship(
        back_populates="task", cascade="all, delete"
    )
    difficulty_level: Mapped[enum.Enum] = mapped_column(
        ENUM("EASY", "MEDIUM", "HARD", name="difficulty_level")
    )  # TODO: check if mapped correctly to enum.Enum, refactor
    votes: Mapped[List["Vote"]] = relationship(
        back_populates="task", cascade="all, delete"
    )
    # author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # author: Mapped["User"] = relationship(back_populates="tasks")


class Solution(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="solutions")
    # author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # author: Mapped["User"] = relationship(back_populates="solutions")
    description: Mapped["SolutionDescription"] = relationship(
        back_populates="solution", cascade="all, delete"
    )
    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False
    )  # TODO: verify
    last_modified: Mapped[datetime] = mapped_column(
        onupdate=datetime.now(), nullable=False
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    # votes


#### Descriptions ####


class DescriptionMixin(object):
    text: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[List[str]] = mapped_column(
        ARRAY(String)
    )  # TODO: verify with real test data in db


class TaskDescription(DescriptionMixin, Base):
    __tablename__ = "task_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="description")
    images: Mapped[List["TaskDescriptionImage"]] = relationship(
        back_populates="task_description", cascade="all, delete"
    )


class SolutionDescription(DescriptionMixin, Base):
    __tablename__ = "solution_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    solution_id: Mapped[int] = mapped_column(ForeignKey("solutions.id"), nullable=False)
    solution: Mapped["Solution"] = relationship(back_populates="description")
    images: Mapped[List["SolutionDescriptionImage"]] = relationship(
        back_populates="solution_description", cascade="all, delete"
    )


#### Images ####


class ImageMixin(object):
    name: Mapped[str] = mapped_column(String, nullable=False)
    # content: Mapped(File) = mapped_column(nullable=False)
    upload_date: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False
    )  # TODO: verify


class TaskDescriptionImage(ImageMixin, Base):
    __tablename__ = "task_description_images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # author: Mapped["User"] = relationship(back_populates="task_description_images")
    task_description_id: Mapped[int] = mapped_column(
        ForeignKey("task_descriptions.id"), nullable=False
    )
    task_description: Mapped["TaskDescription"] = relationship(back_populates="images")


class SolutionDescriptionImage(ImageMixin, Base):
    __tablename__ = "solution_description_images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # author: Mapped["User"] = relationship(back_populates="solution_description_images")
    solution_description_id: Mapped[int] = mapped_column(
        ForeignKey("solution_descriptions.id"), nullable=False
    )
    solution_description: Mapped["SolutionDescription"] = relationship(
        back_populates="images"
    )


#### Testing ####


class TestData(Base):
    __tablename__ = "test_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="test_data")
    test_cases: Mapped[List["TestCase"]] = relationship(
        back_populates="test_data", cascade="all, delete"
    )


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    arguments: Mapped[str] = mapped_column(String, nullable=False)  # TODO:
    expected_result: Mapped[str] = mapped_column(String, nullable=False)  # TODO:
    test_data_id: Mapped[int] = mapped_column(
        ForeignKey("test_data.id"), nullable=False
    )
    test_data: Mapped["TestData"] = relationship(back_populates="test_cases")


#### Tags ####


class TasksTagsAssociation(Base):
    __tablename__ = "tasks_tags"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
    # extra_data: Mapped[Optional[str]]
    task: Mapped["Task"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="tasks")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped["Task"] = relationship(
        "Task", secondary="tasks_tags", back_populates="tags"
    )  # TODO: implement cascade delete


#### ####


class Hint(Base):
    __tablename__ = "hints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="hints")


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stars_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="votes")
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # user: Mapped["User"] = relationship(back_populates="votes")

    __table_args__ = (
        CheckConstraint("0 <= stars_count <= 5", name="check_min_stars_count"),
        # CheckConstraint(stars_count <= 5, name="check_max_stars_count"),
        {},
    )  # TODO: combine checks if possible
