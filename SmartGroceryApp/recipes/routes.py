import os
import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import login_required, current_user
from datetime import date

from ..extensions import db
from ..models import InventoryItem, UserSavedRecipe, SuggestedRecipe
from ..utils.gpt_helpers import generate_recipes_from_ingredients

recipes_bp = Blueprint(
    'recipes',
    __name__,
    url_prefix='/recipes',
    template_folder='templates'
)

API_KEY = os.getenv('SPOONACULAR_API_KEY')
BASE_URL = "https://api.spoonacular.com/recipes"

@recipes_bp.route('/', methods=['GET'])
def recipes_home():
    return redirect(url_for('recipes.get_suggestions'))

@recipes_bp.route('/suggestions', methods=['GET'])
@login_required
def get_suggestions():
    inventory_items = InventoryItem.query.filter_by(user_id=current_user.id).all()
    ingredients = ','.join([item.name for item in inventory_items])

    suggestions_resp = requests.get(f"{BASE_URL}/findByIngredients", params={
        "ingredients": ingredients,
        "number": 5,
        "ranking": 1,
        "apiKey": API_KEY
    })

    suggest_recipes = suggestions_resp.json() if suggestions_resp.status_code == 200 else []

    # Suggested recipes are only retained once
    SuggestedRecipe.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    # Commit new recipes to the SuggestedRecipe table
    for recipe in suggest_recipes:
        suggested = SuggestedRecipe(
            user_id=current_user.id,
            recipe_id=recipe['id'],
            recipe_json=recipe
        )
        db.session.add(suggested)
    db.session.commit()

    saved = UserSavedRecipe.query.filter_by(user_id=current_user.id).all()
    saved_recipes = []
    for s in saved:
        saved_resp = requests.get(f"{BASE_URL}/{s.recipe_id}/information", params={"apiKey": API_KEY})
        if saved_resp.status_code == 200:
            saved_recipes.append(saved_resp.json())

    gpt_recipes = session.pop('gpt_recipes', None)

    return render_template('recipes/index.html',
                           suggest_recipes=suggest_recipes,
                           saved_recipes=saved_recipes,
                           gpt_recipes=gpt_recipes)

@recipes_bp.route('/details/<int:recipe_id>', methods=['GET'])
@login_required
def get_recipe_details(recipe_id):
    response = requests.get(f"{BASE_URL}/{recipe_id}/information", params={
        "includeNutrition": True,
        "apiKey": API_KEY
    })

    if response.status_code == 200:
        recipe = response.json()
        return render_template('recipes/details.html', recipe=recipe)
    return jsonify({"error": "Failed to fetch recipe details"}), 500

@recipes_bp.route('/save/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):   
    existing = UserSavedRecipe.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if existing:
        flash("Recipe already saved.")
        return redirect(url_for('recipes.get_suggestions'))

    recipe = requests.get(f"{BASE_URL}/{recipe_id}/information", params={"apiKey": API_KEY})

    if recipe.status_code == 200:
        saved = UserSavedRecipe(
            user_id=current_user.id, 
            recipe_id=recipe_id, 
            recipe_json=recipe.json(),
            saved_at=date.today()
        )
        db.session.add(saved)
        db.session.commit()
        flash("Recipe saved successfully!")
        return redirect(url_for('recipes.get_suggestions'))

    flash("Failed to save recipe.")
    return redirect(url_for('recipes.get_suggestions'))

@recipes_bp.route('/saved', methods=['GET'])
@login_required
def get_saved_recipes():
    saved = UserSavedRecipe.query.filter_by(user_id=current_user.id).all()
    recipe_ids = [s.recipe_id for s in saved]

    recipes = []
    for rid in recipe_ids:
        response = requests.get(f"{BASE_URL}/{rid}/information", params={"apiKey": API_KEY})
        if response.status_code == 200:
            recipes.append(response.json())

    return jsonify(recipes), 200

@recipes_bp.route('/unsave/<int:recipe_id>', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    saved = UserSavedRecipe.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if saved:
        db.session.delete(saved)
        db.session.commit()
    flash("Recipe removed from saved list.")
    return redirect(url_for('recipes.get_suggestions'))

@recipes_bp.route('/gpt-suggestions', methods=['GET'])
@login_required
def suggest_recipes():
    user_id = current_user.id
    soon_expiring_items = InventoryItem.query.filter(
        InventoryItem.user_id == user_id,
        InventoryItem.expiration_date <= date.today()
    ).all()
    ingredients = [item.name for item in soon_expiring_items]
    if not ingredients:
        session['gpt_recipes'] = []
        return redirect(url_for('recipes.get_suggestions'))

    try:
        recipes = generate_recipes_from_ingredients(ingredients)
        session['gpt_recipes'] = recipes
    except Exception as e:
        session['gpt_recipes'] = [{'error': str(e)}]

    return redirect(url_for('recipes.get_suggestions'))
