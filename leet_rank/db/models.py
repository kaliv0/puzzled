from datetime import datetime
from typing import List

from sqlalchemy import Column

# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from leet_rank.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped["TaskDescription"] = relationship(
        back_populates="task",
        cascade="all, delete",
    )
    test_data: Mapped["TestData"] = relationship(back_populates="task", cascade="all, delete")
    author_solution: Mapped["Solution"] = relationship(back_populates="task", cascade="all, delete")
    user_solutions: Mapped[List["Solution"]] = relationship(
        back_populates="task", cascade="all, delete"
    )
    # =====================
    # author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="tasks")

    # category (list?)
    # tags
    # tips
    # difficulty level
    # votes


class Solution(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="solutions", cascade="all, delete")
    # author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="solutions")
    description: Mapped["SolutionDescription"] = relationship(
        back_populates="solution", cascade="all, delete"
    )
    create_date: Mapped[DateTime] = mapped_column(
        default=datetime.now(), nullable=False
    )  # TODO: verify
    last_modified: Mapped[DateTime] = mapped_column(onupdate=datetime.now(), nullable=False)
    content: Mapped[String] = mapped_column(nullable=False)
    # language
    # votes


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # content = Column(File??)
    upload_date = Column(DateTime, default=datetime.now())  # TODO: verify
    # author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="solutions")


#### Descriptions ####


class DescriptionMixin(object):
    text: Mapped[String] = mapped_column()
    links: Mapped[List[String]] = mapped_column()  # TODO: verify with real test data in db


class TaskDescription(DescriptionMixin, Base):
    __tablename__ = "task_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="description")
    # images = relationship("Image", back_populates="task_description", cascade="all, delete")


class SolutionDescription(DescriptionMixin, Base):
    __tablename__ = "solution_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    solution_id: Mapped[int] = mapped_column(ForeignKey("solutions.id"), nullable=False)
    solution: Mapped["Solution"] = relationship(back_populates="description", cascade="all, delete")
    # images = relationship(
    #     "Image", back_populates="solution_description", cascade="all, delete"
    # )


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
    arguments: Mapped[String] = mapped_column(nullable=False)  # TODO:
    expected_result: Mapped[String] = mapped_column(nullable=False)  # TODO:
    test_data_id: Mapped[int] = mapped_column(ForeignKey("test_data.id"), nullable=False)
    test_data: Mapped["TestData"] = relationship(back_populates="test_cases", cascade="all, delete")
