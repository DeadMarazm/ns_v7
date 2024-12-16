from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import (
    Boolean, Column, DateTime,
    ForeignKey, Integer, String, Text
)
from app.core.extensions import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class UserModel(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(64), unique=True)
    email: Mapped[str] = Column(String(120), unique=True)
    password_hash: Mapped[str] = Column(String(128))
    active: Mapped[bool] = Column(Boolean, default=True)
    confirmed_at: Mapped[datetime] = Column(DateTime, nullable=True)

    roles = relationship("Role", backref="users")
    results = relationship("Result", backref="user")


class RoleModel(db.Model):
    __tablename__ = "role"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(80), unique=True)
    description: Mapped[str] = Column(String(255))


class WorkoutModel(db.Model):
    __tablename__ = "workout"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    warm_up: Mapped[str] = Column(Text, nullable=False)
    workout: Mapped[str] = Column(Text, nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    date_posted: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)

    results = relationship("Result", backref="workout")


class ResultModel(db.Model):
    __tablename__ = "result"

    id: Mapped[int] = Column(Integer, primary_key=True)
    confirm: Mapped[bool] = Column(Boolean)
    date_posted: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))
    workout_id: Mapped[int] = Column(Integer, ForeignKey("workout.id"))
