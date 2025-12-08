
from .extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    inventory_items = db.relationship('InventoryItem', backref='user', lazy=True)
    saved_recipes = db.relationship('UserSavedRecipe', backref='user', lazy=True)
    reports = db.relationship('Report', backref='user', lazy=True)


class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    quantity = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# class Recipe(db.Model):
#     __tablename__ = 'recipes'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     ingredients = db.Column(db.Text, nullable=False)  # Consider JSON or separate table for normalization
#     instructions = db.Column(db.Text, nullable=False)
#     macros = db.Column(db.String(255), nullable=True)  # JSON string (e.g., {"calories": 200, "protein": 15})


class UserSavedRecipe(db.Model):
    __tablename__ = 'user_saved_recipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, primary_key=True)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    recipe_json = db.Column(db.JSON, nullable=False)

class SuggestedRecipe(db.Model):
    __tablename__ = 'suggested_recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    recipe_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    # Relationships
    user = db.relationship('User', backref='suggested_recipes')
    # recipe = db.relationship('Recipe', backref='suggested_entries')

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    data_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))