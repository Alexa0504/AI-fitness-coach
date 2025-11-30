from datetime import datetime, timezone, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, event
from sqlalchemy.types import JSON as SQLiteJSON
from sqlalchemy.dialects.postgresql import JSONB
import json
import os

db = SQLAlchemy()

JSONColumn = db.JSON if os.environ.get("TESTING") == "1" else JSONB

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    goals = db.relationship("Goal", backref="user", cascade="all, delete-orphan")
    plans = db.relationship("Plan", backref="user", cascade="all, delete-orphan")

    xp = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    progress_saved_state = db.Column(JSONColumn, default=dict)
    last_progress_update = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    target_weight_kg = db.Column(db.Float, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_progress_state(self):
        if isinstance(self.progress_saved_state, str):
            try:
                return json.loads(self.progress_saved_state)
            except Exception:
                return {}
        return self.progress_saved_state or {}

    def set_progress_state(self, obj):
        if isinstance(self.progress_saved_state, str):
            self.progress_saved_state = json.dumps(obj)
        else:
            self.progress_saved_state = obj

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "xp": self.xp,
            "level": self.level,
            "progress_saved_state": self.get_progress_state(),
            "last_progress_update": self.last_progress_update.isoformat() if self.last_progress_update else None,
            "created_at": self.created_at.isoformat(),
            "gender": self.gender,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "target_weight_kg": self.target_weight_kg,
            "age": self.age
        }

class UserGoal(db.Model):
    __tablename__ = "user_goals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_name = db.Column(db.String(255), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "goal_name": self.goal_name,
            "week_start": self.week_start.isoformat() if self.week_start else None,
            "is_completed": self.is_completed
        }

class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Goal {self.goal_type} for User {self.user_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "goal_type": self.goal_type,
            "target_value": self.target_value,
            "unit": self.unit,
            "created_at": self.created_at.isoformat(),
        }

class Plan(db.Model):
    __tablename__ = "plans"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    content = db.Column(db.JSON, nullable=True)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Plan {self.plan_type} for User {self.user_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan_type": self.plan_type,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "content": self.content,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
        }

class TokenBlacklist(db.Model):
    __tablename__ = "token_blacklist"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TokenBlacklist {self.token}>"

class Tip(db.Model):
    __tablename__ = "tips"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Tip {self.text[:20]}>"

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "text": self.text
        }

if os.environ.get("TESTING") == "1":
    @event.listens_for(User.__table__, "before_create")
    def replace_jsonb_column(target, connection, **kw):
        for col in target.columns:
            if col.name == "progress_saved_state":
                col.type = SQLiteJSON
