from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = relationship(
        "TaskDescription",
        back_populates="task",
        cascade="all, delete",
    )
    test_data = relationship(
        "TaskDescription", back_populates="task", cascade="all, delete"
    )
    author_solution_id = Column(Integer, ForeignKey("solutions.id"), nullable=False)
    author_solution = relationship(
        "Solution", back_populates="task", cascade="all, delete"
    )
    user_solutions = relationship(
        "Solution", back_populates="task", cascade="all, delete"
    )
    # author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="tasks")

    # category (list?)
    # tags
    # tips
    # difficulty level
    # votes


class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task = relationship("Task", back_populates="solutions", cascade="all, delete")
    # author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="solutions")
    description_id = Column(Integer, ForeignKey("descriptions.id"), nullable=False)
    description = relationship(
        "Description", back_populates="solutions", cascade="all, delete"
    )
    create_date = Column(DateTime, default=datetime.now())  # TODO: verify
    last_modified = (Column(DateTime, onupdate=datetime.now()),)
    content = Column(String, nullable=False)
    # language
    # votes


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # content = Column(File??)
    upload_date = Column(DateTime, default=datetime.now())  # TODO: verify
    # author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="solutions")


class DescriptionMixin(object):
    text = Column(String)
    links = Column(ARRAY(String))


class TaskDescription(DescriptionMixin, Base):
    __tablename__ = "task_descriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task = relationship("Task", back_populates="description")
    # task = relationship("Task", back_populates="description", backref=backref("items", cascade="all, delete-orphan"))
    images = relationship(
        "Image", back_populates="task_description", cascade="all, delete"
    )


class SolutionDescription(DescriptionMixin, Base):
    __tablename__ = "solution_descriptions"

    solution_id = Column(Integer, ForeignKey("solutions.id"))
    solution = relationship("Solution", back_populates="description")
    images = relationship(
        "Image", back_populates="solution_description", cascade="all, delete"
    )


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    arguments = Column(String)  # TODO:
    expected_result = Column(String)  # TODO:
    test_data_id = Column(Integer, ForeignKey("test_data.id"), nullable=False)
    test_data = relationship("TestData", back_populates="test_cases")


class TestData(Base):
    __tablename__ = "test_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task = relationship("Task", back_populates="test_data")
    test_cases = relationship(
        "TestCase", back_populates="test_data", cascade="all, delete"
    )
