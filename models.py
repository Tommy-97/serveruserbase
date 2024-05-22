
from sqlalchemy import (Column, Date, DateTime, ForeignKey, Integer, String,
                        Time, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql+psycopg2://имяюзера:пароль@localhost/имябазы"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    tasks = relationship("Task", back_populates="user")
    teams = relationship("Team", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")


class Norm(Base):
    __tablename__ = "norms"

    id = Column(Integer, primary_key=True, index=True)
    equipment = Column(String, index=True)
    work_type = Column(String, index=True)
    setup_time = Column(Integer)
    productivity_per_hour = Column(Integer)


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    equipment = Column(String, index=True)
    date = Column(Date)
    shifts = Column(String)


class Break(Base):
    __tablename__ = "breaks"

    id = Column(Integer, primary_key=True, index=True)
    break_start = Column(Time)
    break_duration = Column(Integer)
    shift_type = Column(String)


class Planning(Base):
    __tablename__ = "planning"

    id = Column(Integer, primary_key=True, index=True)
    equipment = Column(String, index=True)
    work_type = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    actual_end_time = Column(DateTime, nullable=True)
    priority = Column(Integer)

    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="plannings")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    priority = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))

    user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    plannings = relationship("Planning", back_populates="task")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    start = Column(DateTime)
    factual_end = Column(DateTime, nullable=True)
    plan_end = Column(DateTime)

    tasks = relationship("Task", back_populates="project")
    teams = relationship("Team", back_populates="project")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    creation_date = Column(Date)
    disbandment_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="teams")
    project = relationship("Project", back_populates="teams")


Base.metadata.create_all(bind=engine)
