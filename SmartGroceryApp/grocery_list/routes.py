
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from ..extensions import db
from SmartGroceryApp.models import UserSavedRecipe, InventoryItem, SuggestedRecipe
from SmartGroceryApp.inventory.routes import GROCERY_CATEGORIES

import json



grocery_bp = Blueprint(
    'grocery',
    __name__, 
    url_prefix='/grocery',
    template_folder='templates'
    )

# @grocery_bp.route('/generate', methods=['GET'])
# @jwt_required()
# def generate_grocery_list():
#     user_id = get_jwt_identity()
#     # Mock: Replace with real logic combining planned meals & inventory gaps
#     return jsonify([
#         {"name": "Tomatoes", "quantity": 5},
#         {"name": "Milk", "quantity": 1}
#     ])

# @grocery_bp.route('/', methods=['GET'])
# def grocery_home():
#     #return "<h1>Grocery List Generator</h1>"
#     return render_template('grocery/index.html')

@grocery_bp.route('/')
@login_required
# @jwt_required()
def grocery_list_home():
    # Create a list of groceries
    all_ingredients = get_grocery_list(current_user.id)
    return render_template('grocery/index.html', 
                           grocery_items=sorted(all_ingredients), 
                           categories=GROCERY_CATEGORIES)


@grocery_bp.route('/add', methods=["POST"])
@login_required
# @jwt_required()
def add_item():
    """
    Adds grocery list items to user's inventory
    """
    name = request.form['name']
    quantity = request.form['quantity']
    expiration_date_str = request.form.get('expiration_date')
    category = request.form.get('category', '')

    new_item = InventoryItem(
        user_id=current_user.id,
        name=name,
        quantity=quantity,
        expiration_date=datetime.strptime(expiration_date_str, '%Y-%m-%d').date(),
        category=category
    )
    db.session.add(new_item)
    db.session.commit()
    flash(f'{name} added to your inventory.', 'success')
    return redirect(url_for('grocery.grocery_list_home'))

def get_grocery_list(user_id):
    # Get saved recipe IDs for user
    saved_recipe_ids = [saved.recipe_id for saved in UserSavedRecipe.query.filter_by(user_id=user_id).all()]

    # Get user's current inventory items
    inventory_items = InventoryItem.query.filter_by(user_id=user_id).all()
    seen = {item.name.strip().lower() for item in inventory_items}

    # Get all the ingredients not in the inventory for saved recipes
    all_ingredients = []
    for recipe_id in saved_recipe_ids:
        suggested = SuggestedRecipe.query.filter_by(recipe_id=recipe_id, user_id=user_id).first()
        if suggested:
            recipe_data = suggested.recipe_json
            for ingredient in recipe_data.get('missedIngredients', []):
                name = ingredient['name'].lower()
                if name not in seen:
                    all_ingredients.append(ingredient['name'])
                    seen.add(name)
    return all_ingredients


# @grocery_bp.route('/api', methods=['GET'])
# @login_required
# def grocery_list_api():
#     """Return grocery list as JSON"""
#     saved_recipe_ids = [saved.recipe_id for saved in UserSavedRecipe.query.filter_by(user_id=current_user.id).all()]
#     all_ingredients = []
#     for recipe in Recipe.query.filter(Recipe.id.in_(saved_recipe_ids)).all():
#         try:
#             ingredients = json.loads(recipe.ingredients)
#             all_ingredients.extend(ingredients)
#         except json.JSONDecodeError:
#             continue

#     required_ingredients = set(item.lower() for item in all_ingredients)
#     user_inventory = set(item.name.lower() for item in InventoryItem.query.filter_by(user_id=current_user.id).all())
#     missing_ingredients = required_ingredients - user_inventory

#     return jsonify(sorted(missing_ingredients))