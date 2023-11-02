from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from db.database import Base
from sqlalchemy import Column


# class DbUser(Base):
#   __tablename__ = 'users'
#   id = Column(Integer, primary_key=True, index=True)
#   username = Column(String)
#   email = Column(String)
#   password = Column(String)
#   items = relationship('DbArticle', back_populates='user')

# class DbArticle(Base):
#   __tablename__= 'articles'
#   id = Column(Integer, primary_key=True, index=True)
#   title = Column(String)
#   content = Column(String)
#   published = Column(Boolean)
#   user_id = Column(Integer, ForeignKey('users.id'))
#   user = relationship("DbUser", back_populates='items')


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
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="description")
    # task = relationship("Task", back_populates="description", backref=backref("items", cascade="all, delete-orphan"))


# class SolutionDescription(DescriptionMixin, Base):
#     __tablename__ = "solution_descriptions"

#     solution_id = Column(Integer, ForeignKey("solutions.id"))
#     solution = relationship("Task", back_populates="description")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = relationship(
        "TaskDescription",
        back_populates="task",
        cascade="all, delete",
    )
    # test data (IO for tests)
    # author's solution (optional)
    # category (list?)
    # tags
    # tips
    # difficulty level
    # solutions
    # author
    # votes
