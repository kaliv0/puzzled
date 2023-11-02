from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

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
    # author's solution (optional)
    # category (list?)
    # tags
    # tips
    # difficulty level
    # solutions
    # author
    # votes


# class Image(Base):
#     __tabelname__ = "images"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     content: Mapped[bytearray] = mapped_column()


class DescriptionMixin(object):
    text = Column(String)
    # images: Mapped[List[Image]] = mapped_column()
    # links: Mapped[List[str]] = mapped_column()


class TaskDescription(DescriptionMixin, Base):
    __tablename__ = "task_descriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    task = relationship("Task", back_populates="description")
    # task = relationship("Task", back_populates="description", backref=backref("items", cascade="all, delete-orphan"))


# class SolutionDescription(DescriptionMixin, Base):
#     __tablename__ = "solution_descriptions"

#     solution_id = Column(Integer, ForeignKey("solutions.id"))
#     solution = relationship("Task", back_populates="description")


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
