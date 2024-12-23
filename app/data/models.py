from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import (
    Boolean, Column, DateTime,
    ForeignKey, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.extensions import Base
import uuid


class RolesUsers(Base):
    """Модель связи между ролями и пользователями."""
    __tablename__ = 'roles_users'
    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), primary_key=True)
    role_id: Mapped[int] = Column(Integer, ForeignKey('role.id'), primary_key=True)


class User(Base):
    """Модель пользователя."""
    __tablename__ = "user"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = Column(String(64), unique=True, nullable=False)
    email: Mapped[str] = Column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = Column(String(128), nullable=False)
    active: Mapped[bool] = Column(Boolean, default=True)
    confirmed_at: Mapped[datetime] = Column(DateTime, nullable=True)
    uuid: Mapped[uuid.UUID] = Column(PG_UUID(as_uuid=True), unique=True, default=uuid.uuid4)

    roles: Mapped[list["Role"]] = relationship("Role", secondary="roles_users", back_populates="users")
    results: Mapped[list["Result"]] = relationship("Result", back_populates="user")


class Role(Base):
    """Модель роли."""
    __tablename__ = "role"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(80), unique=True, nullable=False)
    description: Mapped[str] = Column(String(255))

    users: Mapped[list["User"]] = relationship("User", secondary="roles_users", back_populates="roles")


class Workout(Base):
    """Модель тренировки."""
    __tablename__ = "workout"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    warm_up: Mapped[str] = Column(Text, nullable=False)
    workout: Mapped[str] = Column(Text, nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    date_posted: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)

    results: Mapped[list["Result"]] = relationship("Result", back_populates="workout")


class Result(Base):
    """Модель результата тренировки."""
    __tablename__ = "result"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    confirm: Mapped[bool] = Column(Boolean)
    date_posted: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"), nullable=False)
    workout_id: Mapped[int] = Column(Integer, ForeignKey("workout.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="results")
    workout: Mapped["Workout"] = relationship("Workout", back_populates="results")
