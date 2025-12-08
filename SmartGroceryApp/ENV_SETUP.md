
# Environment Configuration (.env)

This application uses a `.env` file to manage environment-specific settings securely.

## 🚫 Do NOT commit `.env` to Git

The `.env` file contains **sensitive information**, such as database credentials and secret keys. It should always be added to `.gitignore` and **never committed to version control**.

---

## 📄 .env.example

This project includes a `.env.example` file. It is a **template** that shows which environment variables are required to run the application.

### Example `.env.example` contents:

```env
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
DATABASE_URL=sqlite:///smart_grocery.db
```

---

## ✅ How to use

1. Copy `.env.example` to a new file named `.env` in the root directory:
   ```bash
   cp .env.example .env
   ```

2. Fill in the required values in `.env`.

3. The application will automatically load the variables from `.env` using `python-dotenv`.

---

## ⚙️ Flask App Setup

Make sure you have `python-dotenv` installed:
```bash
pip install python-dotenv
```

And that your `config.py` includes:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🔐 Keep Secrets Safe

Do not expose your `.env` file or include real credentials in public repositories or screenshots.

