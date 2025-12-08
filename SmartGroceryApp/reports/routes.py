from flask import render_template, jsonify, Blueprint
from datetime import timedelta, date
from flask_login import login_required, current_user
from ..extensions import db

# Smart Grocery App imports
from SmartGroceryApp.models import InventoryItem, UserSavedRecipe
from SmartGroceryApp.grocery_list.routes import get_grocery_list
from SmartGroceryApp.inventory.routes import count_inventory

reports_bp = Blueprint(
    'reports',
    __name__,
    url_prefix='/reports',
    template_folder='templates'
    )

@reports_bp.route('/', methods=['GET'])
@login_required
def reports_home():
    now = date.today()
    week_ago = now - timedelta(days=7)
    soon = now + timedelta(days=3)

    # used_items = InventoryItem.query.filter(
    #     InventoryItem.user_id == current_user.id,
    #     InventoryItem.added_at >= week_ago
    # ).all()

    saved_recipes = UserSavedRecipe.query.filter(
        UserSavedRecipe.user_id == current_user.id,
        UserSavedRecipe.saved_at >= week_ago
    ).all()

    all_ingredients = get_all_ingredients(saved_recipes)
    used_items = get_used_items(all_ingredients)
    print("Used Items:", used_items)

    expiring_items = InventoryItem.query.filter(
        InventoryItem.user_id == current_user.id,
        InventoryItem.expiration_date <= soon
    ).all()

    expired_items = InventoryItem.query.filter(
        InventoryItem.user_id == current_user.id,
        InventoryItem.expiration_date < now
    ).all()
    recipe_titles = [r.recipe_json.get('title', 'Unnamed Recipe') for r in saved_recipes]


    return render_template(
        'reports/index.html',
        used_items=used_items,
        saved_recipes=recipe_titles,
        expiring_items=expiring_items,
        expired_items=expired_items,
        grocery_list=get_grocery_list(current_user.id),
        category_counts=count_inventory(current_user.id)
    )

@reports_bp.route('/weekly-summary', methods=['GET'])
@login_required
def weekly_summary():
    now = date.today()
    week_ago = now - timedelta(days=7)

    used_items = InventoryItem.query.filter(
        InventoryItem.user_id == current_user.id,
        InventoryItem.added_at >= week_ago
    ).all()

    saved_recipes = UserSavedRecipe.query.filter(
        UserSavedRecipe.user_id == current_user.id,
        UserSavedRecipe.saved_at >= week_ago
    ).all()

    summary = {
        "used_items": [item.name for item in used_items],
        "saved_recipes": [r.recipe.name for r in saved_recipes if r.recipe]
    }

    return jsonify(summary), 200


@reports_bp.route('/expiring-items', methods=['GET'])
@login_required
def expiring_items():
    now = date.today()
    soon = now + timedelta(days=3)

    expiring = InventoryItem.query.filter(
        InventoryItem.user_id == current_user.id,
        InventoryItem.expiration_date <= soon
    ).all()

    result = [
        {"name": item.name, "expires": item.expiration_date.strftime('%Y-%m-%d')}
        for item in expiring
    ]

    return jsonify(result), 200


@reports_bp.route('/waste-tracker', methods=['GET'])
@login_required
def waste_tracker():
    now = date.today()

    expired_items = InventoryItem.query.filter(
        InventoryItem.user_id == current_user.id,
        InventoryItem.expiration_date < now
    ).all()

    wasted = [
        {"name": item.name, "expired_on": item.expiration_date.strftime('%Y-%m-%d')}
        for item in expired_items
    ]

    return jsonify(wasted), 200


    
def get_all_ingredients(recent_saved):
    # Extract all ingredient names from recent recipe JSONs
    all_ingredients = set()
    for saved in recent_saved:
        ingredients = saved.recipe_json.get('usedIngredients') or saved.recipe_json.get('extendedIngredients') or []
        for ing in ingredients:
            name = ing.get('name')
            if name:
                all_ingredients.add(name.lower())
    return all_ingredients

def get_used_items(all_ingredients):
    inventory_items = InventoryItem.query.filter_by(user_id=current_user.id).all()
    used_items = [item for item in inventory_items if item.name.lower() in all_ingredients]
    return used_items

# def get_expiring_items:():

