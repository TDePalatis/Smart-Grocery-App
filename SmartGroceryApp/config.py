import os
from dotenv import load_dotenv

# Load .env parameters
load_dotenv()

# Ensure the instance folder exists
os.makedirs("instance", exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "defaultjwtkey")
    SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY", "defaultspoonacularkey")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///instance/dev.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'pass')
    MYSQL_DB = os.getenv('MYSQL_DB', 'grocerydb')

    # SQLALCHEMY_DATABASE_URI = (
    #     f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    # )

