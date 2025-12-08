import requests
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, date

# Import Database
from ..models import InventoryItem
from ..extensions import db

# Import JSON Schema and Schema Validation
from jsonschema.exceptions import ValidationError
from SmartGroceryApp.validators.validator import JSONSchemaValidator
validator = JSONSchemaValidator()

GROCERY_CATEGORIES = [
    "Produce",
    "Dairy",
    "Meat",
    "Bakery",
    "Frozen",
    "Pantry",
    "Beverages",
    "Snacks",
    "Condiments",
    "Spices",
    "Other"
]

inventory_bp = Blueprint(
    'inventory',
    __name__,
    url_prefix='/inventory',
    template_folder='templates'
)

@inventory_bp.route('/', methods=['GET', 'POST'])
@login_required
def inventory_home():
    user_id = current_user.id
    edit_item = None  # Track item being edited

    # Handle form submission
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        delete_id = request.form.get('delete_id')

        # Handle deletion
        if delete_id:
            item = InventoryItem.query.get(delete_id)
            if item and item.user_id == user_id:
                db.session.delete(item)
                db.session.commit()
            return redirect(url_for('inventory.inventory_home'))

        # Editing mode — just pre-fill form
        if item_id and not request.form.get('name'):
            edit_item = InventoryItem.query.get(item_id)
        else:
            # Handle add or edit
            name = request.form.get('name')
            quantity = request.form.get('quantity')
            category = request.form.get('category')
            expiration_date_str = request.form.get('expiration_date')
            expiration_date = None
            if expiration_date_str:
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()

            # Edit Existing Item
            if item_id:
                item = InventoryItem.query.get(item_id)
                added_at = item.added_at
                if item and item.user_id == user_id:
                    # Fallback to current values if inputs are empty
                    item.name = name if name else item.name
                    item.quantity = quantity if quantity else item.quantity
                    item.category = category if category else item.category
                    item.added_at = added_at if added_at else date.today()
                    if expiration_date:
                        item.expiration_date = expiration_date

            # Add new Item
            else:
                # Prevent inserting NULL name or quantity
                if not name or not quantity:
                    inventory_items = InventoryItem.query.filter_by(user_id=user_id).all()
                    return render_template("inventory/inventory.html", 
                                           inventory=inventory_items,
                                           categories = GROCERY_CATEGORIES,
                                           error="Name and quantity required.")
                item = InventoryItem(
                    name=name,
                    quantity=quantity,
                    expiration_date=expiration_date,
                    category=category,
                    user_id=user_id,
                    added_at=date.today()
                )
                db.session.add(item)
            db.session.commit()
            return redirect(url_for('inventory.inventory_home'))          
    
    # GET Request from lookup_barcode
    item_name = request.args.get('name')

    # Fetch current inventory
    inventory_items = InventoryItem.query.filter_by(user_id=user_id).all()

    # Add days left calculation
    for item in inventory_items:
        item.days_left = (item.expiration_date - date.today()).days if item.expiration_date else "N/A"

    return render_template('inventory/inventory.html',
                           categories = GROCERY_CATEGORIES, 
                           inventory=inventory_items, 
                           edit_item=edit_item, 
                           name=item_name)

@inventory_bp.route('/lookup_barcode', methods=['POST'])
def lookup_barcode():
    barcode = request.form.get('barcode')
    if not barcode:
        flash("Barcode is required.")
        return redirect(url_for('inventory.inventory_home'))

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200 or 'product' not in response.json():
        flash("Product not found.")
        return redirect(url_for('inventory.inventory_home'))

    product = response.json()['product']
    name = product.get('product_name', 'Unknown')

    # redirect to inventory home with found item name
       # redirect to inventory home with found item name
    return redirect(url_for('inventory.inventory_home', name = name))

def count_inventory(user_id):
    # Initialize the count dictionary
    category_counts = {category: 0 for category in GROCERY_CATEGORIES}

    # Query all inventory items for the current user
    items = InventoryItem.query.filter_by(user_id=user_id).all()

    # Count items by category
    for item in items:
        if item.category in category_counts:
            category_counts[item.category] += 1
        else:
            category_counts["Other"] += 1

    return category_counts

# VALIDATION BACKEND
#         try:
#             validator.validate(form_data, "grocery_item")
#             return render_template("inventory/add_item.html", message="Item added successfully!")
#         except ValidationError as e:
#             return render_template("inventory/add_item.html", error="Validation failed.", details=str(e))

# VALIDATION FRONTEND
#   {% if message %}
#     <p style="color:green;">{{ message }}</p>
#   {% elif error %}
#     <p style="color:red;">{{ error }}</p>
#     <pre style="color:red;">{{ details }}</pre>
#   {% endif %}