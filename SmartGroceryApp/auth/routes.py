from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..extensions import db
from flask_jwt_extended import create_access_token
from datetime import timedelta
from jsonschema.exceptions import ValidationError
from SmartGroceryApp.validators.validator import JSONSchemaValidator

validator = JSONSchemaValidator()

auth_bp = Blueprint(
    'auth', 
    __name__, 
    url_prefix='/auth',
    template_folder='templates'
)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        try:
            validator.validate(form_data, "user")

            # Check if user already exists
            if User.query.filter_by(email=form_data['email']).first():
                return render_template("auth/register.html", error='Email already exists.')

            # Create new user
            user = User(
                email=form_data['email'],
                password_hash=generate_password_hash(form_data['password'])
            )
            db.session.add(user)
            db.session.commit()

            print(f"User {user.email} created with ID {user.id}")
            login_user(user)

            # Redirect to the reports dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('reports.reports_home'))

        except ValidationError as e:
            flash('Incorrect email or password.')
            return render_template("auth/register.html", error="Validation failed.", details=str(e))

    # GET method fallback
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        try:
            validator.validate(form_data, "user")
            user = User.query.filter_by(email=form_data['email']).first()
            if user and check_password_hash(user.password_hash, form_data['password']):
                login_user(user)
                return redirect(url_for('reports.reports_home'))

            return render_template("auth/login.html", error='Incorrect email or password.')

        except ValidationError as e:
            return render_template("auth/login.html", error="Validation failed.", details=str(e))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# @auth_bp.route('/reports', methods=['GET', 'POST'])
# @login_required
# def reports():
#     return render_template('reports/index.html', user=current_user)

@auth_bp.route('/', methods=['GET'])
def auth_home():
    return render_template('auth/login.html')
