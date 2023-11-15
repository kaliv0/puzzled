import enum
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import UploadFile
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import CheckConstraint, ForeignKey
from sqlalchemy.sql.sqltypes import Enum, Integer, LargeBinary, String


class Base(DeclarativeBase):
    pass


# #### Enums ####


class DifficultyLevel(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Role(str, enum.Enum):
    USER = "USER"
    STAFF = "STAFF"
    ADMIN = "ADMIN"


# #### Tasks ####


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped["TaskDescription"] = relationship(
        back_populates="task",
        cascade="all, delete",
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
        Enum(DifficultyLevel, name="difficulty_levels")
    )
    create_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    last_modified: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),  # TODO: make equal to create_date vs calling utcnow()
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    votes: Mapped[List["TaskVote"]] = relationship(
        back_populates="task", cascade="all, delete"
    )
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["User"] = relationship(back_populates="tasks")


# #### Solutions ####


class Solution(Base):
    __tablename__ = "solutions"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="solutions")
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["User"] = relationship(back_populates="solutions")
    description: Mapped["SolutionDescription"] = relationship(
        back_populates="solution", cascade="all, delete"
    )
    create_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    last_modified: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),  # TODO: make equal to create_date vs calling utcnow()
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    votes: Mapped[List["SolutionVote"]] = relationship(
        back_populates="solution", cascade="all, delete"
    )


# #### Descriptions ####


class DescriptionMixin(object):
    text: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])


class TaskDescription(DescriptionMixin, Base):
    __tablename__ = "task_descriptions"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="description")
    images: Mapped[List["TaskDescriptionImage"]] = relationship(
        back_populates="task_description", cascade="all, delete"
    )


class SolutionDescription(DescriptionMixin, Base):
    __tablename__ = "solution_descriptions"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    solution_id: Mapped[UUID] = mapped_column(
        ForeignKey("solutions.id"), nullable=False
    )
    solution: Mapped["Solution"] = relationship(back_populates="description")
    images: Mapped[List["SolutionDescriptionImage"]] = relationship(
        back_populates="solution_description", cascade="all, delete"
    )


# #### Images ####


class ImageMixin(object):
    name: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[UploadFile] = mapped_column(LargeBinary, nullable=False)
    upload_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )


class TaskDescriptionImage(ImageMixin, Base):
    __tablename__ = "task_description_images"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    task_description_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_descriptions.id"), nullable=False
    )
    task_description: Mapped["TaskDescription"] = relationship(back_populates="images")


class SolutionDescriptionImage(ImageMixin, Base):
    __tablename__ = "solution_description_images"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    solution_description_id: Mapped[UUID] = mapped_column(
        ForeignKey("solution_descriptions.id"), nullable=False
    )
    solution_description: Mapped["SolutionDescription"] = relationship(
        back_populates="images"
    )


class ProfileImage(ImageMixin, Base):
    __tablename__ = "profile_images"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="profile_picture")


# #### Tags ####


class TasksTagsAssociation(Base):
    __tablename__ = "tasks_tags"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"), primary_key=True)
    task: Mapped["Task"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="tasks")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped["Task"] = relationship(
        "Task", secondary="tasks_tags", back_populates="tags"
    )  # TODO: implement cascade delete


# #### Hints ####


class Hint(Base):
    __tablename__ = "hints"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="hints")


# #### Votes ####


class VoteMixin(object):
    stars_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TaskVote(VoteMixin, Base):
    __tablename__ = "task_votes"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="votes")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="task_votes")

    __table_args__ = (
        CheckConstraint("stars_count >= 0", name="check_min_stars_count"),
        CheckConstraint("stars_count <= 5", name="check_max_stars_count"),
        {},
    )


class SolutionVote(VoteMixin, Base):
    __tablename__ = "solution_votes"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    solution_id: Mapped[UUID] = mapped_column(
        ForeignKey("solutions.id"), nullable=False
    )
    solution: Mapped["Solution"] = relationship(back_populates="votes")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="solution_votes")

    __table_args__ = (
        CheckConstraint("stars_count >= 0", name="check_min_stars_count"),
        CheckConstraint("stars_count <= 5", name="check_max_stars_count"),
        {},
    )


# #### Users ####


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(
        String
    )  # nullable by default # TODO: decide for max length
    nickname: Mapped[str] = mapped_column(
        String, nullable=False
    )  # TODO: decide for max length
    # TODO: add validation for email?
    email: Mapped[str] = mapped_column(String)
    # TODO: add hashing and validation
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_picture: Mapped[ProfileImage] = relationship(
        back_populates="user", cascade="all, delete"
    )
    about: Mapped[str] = mapped_column(String)  # TODO: decide for max length
    join_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    last_login: Mapped[datetime] = mapped_column(
        # TODO: make default = join_date?
        default=datetime.utcnow(),
        nullable=False,
    )
    task_stars_received: Mapped[int] = mapped_column(Integer, default=0)
    solution_stars_received: Mapped[int] = mapped_column(Integer, default=0)
    solutions: Mapped[List["Solution"]] = relationship(
        back_populates="author", cascade="all, delete"
    )
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="author", cascade="all, delete"
    )
    task_votes: Mapped[List["TaskVote"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    solution_votes: Mapped[List["SolutionVote"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    role: Mapped[Role] = mapped_column(Enum(Role, name="user_roles"))
