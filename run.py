import os
import pymysql
from SmartGroceryApp import create_app
from SmartGroceryApp.config import DevelopmentConfig, TestingConfig, ProductionConfig

env = os.getenv("FLASK_ENV", "development")


# Optional: load .env if not using Flask CLI
from dotenv import load_dotenv
load_dotenv()

def create_mysql_database_if_missing():
    if env != "production":
        return

    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    dbname = os.getenv("MYSQL_DB")

    # Connect without specifying database
    conn = pymysql.connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
    print(f"✔️ Ensured database `{dbname}` exists.")
    cursor.close()
    conn.close()

def apply_schema_sql():
    if env != "production":
        return

    dbname = os.getenv("MYSQL_DB")
    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    schema_path = os.path.join("SmartGroceryApp", "smart_grocery_schema.sql")

    if not os.path.isfile(schema_path):
        print(f"❌ Schema file not found: {schema_path}")
        return

    with open(schema_path, "r") as f:
        sql_statements = f.read().split(";")

    conn = pymysql.connect(host=host, user=user, password=password, database=dbname)
    cursor = conn.cursor()
    for stmt in sql_statements:
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"⚠️ Error running SQL: {stmt}\n{e}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✔️ Applied schema from {schema_path}")

# --- Auto-setup for production ---
if env == "production":
    create_mysql_database_if_missing()
    apply_schema_sql()

# Then start Flask app
if env == "production":
    app = create_app(ProductionConfig)
elif env == "testing":
    app = create_app(TestingConfig)
else:
    app = create_app(DevelopmentConfig)

# Debug print to verify the database path
print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])

if __name__ == "__main__":
    app.run(debug=(env != "production"))
