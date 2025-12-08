# Smart Grocery App Database Management
1. Development  
`FLASK_ENV=development flask run`

2. Testing (Pytest will use TestingConfig)  
`pytest`

3. Production (e.g., via gunicorn)  
`FLASK_ENV=production gunicorn run:app`

## Development
```mermaid
flowchart TD
  A1[FLASK_ENV=dev] --> B1[DevelopmentConfig]
  B1 --> C1[sqlite:///instance/dev.db]
  B1:::config --> C1:::db
  B1:::config --> note1["Uses local SQLite<br>db.create_all() on boot"]
  C1:::db --> note2["Tables auto-created<br>Easy reset, no server"]

  classDef config fill:#f9f,stroke:#333,stroke-width:1px;
  classDef db fill:#bbf,stroke:#333,stroke-width:1px;
```
The development database is set to be created in `./instance/dev.db` using `SQLAlchemy`.

The command `db.create_all()` is used to create the temporary database as defined by in `models.py`.

## Testing
```mermaid
flowchart TD
  A2[FLASK_ENV=test] --> B2[TestingConfig]
  B2 --> C2[sqlite:///:memory:]
  B2:::config --> note3["In-memory SQLite<br>db.create_all() in tests"]
  C2:::db --> note4["Fast, isolated for pytest<br>Auto-rollback after test"]

  classDef config fill:#f9f,stroke:#333,stroke-width:1px;
  classDef db fill:#bbf,stroke:#333,stroke-width:1px;
```
TBD

## Production
The production database will us mySQL.  
The schema is defined in `smart_grocery_schema.sql`

```mermaid
flowchart TD
  A3[FLASK_ENV=prod] --> B3[ProductionConfig]
  B3 --> C3[mysql+pymysql://...]
  B3:::config --> note5["Uses MySQL via .env<br>or cloud secret storage"]
  C3:::db --> note6["Must apply schema manually<br>`flask db upgrade` (if used)"]

  classDef config fill:#f9f,stroke:#333,stroke-width:1px;
  classDef db fill:#bbf,stroke:#333,stroke-width:1px;
```
### Local Testing
`mysql -u your_user -p your_database < smart_grocery_schema.sql
`

### Deployment
TBD