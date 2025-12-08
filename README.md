# 🧠 Smart Grocery Housekeeping App
This is a web-based application designed for the **CS467 Capstone Project** at Oregon State University. The goal is to explore the **maximum possible use of AI tools** while developing a functional app that reduces household food waste through intelligent grocery tracking and recipe suggestions.

---


## 📌 Project Overview
In today’s fast-paced world, groceries often go unused and spoil. Our app helps users:
- Record groceries via manual entry, barcode scanning, or image recognition
- Get notified about items nearing expiration
- Receive recipe suggestions based on current pantry inventory
- Track frequently used, spoiled, or unused items
We built this app while documenting the entire process of using AI tools such as ChatGPT, GitHub Copilot, Google Teachable Machine, and more.


## 📦 Features

- **Grocery Recognition**: Upload or capture images to identify grocery items using a trained TensorFlow model.
- **Recipe Suggestions**: Suggests recipes based on inventory using GPT and Spoonacular API.
- **Inventory Tracking**: Manually or automatically update item status (used/spoiled).
- **Reports**: Usage insights, spoilage tracking, and frequently used item reports.
- **User Auth**: Secure login system with Flask-Login & JWT support.
- **Responsive UI**: Template-driven Flask frontend with support for multiple pages.

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, Jinja2, CSS, JS
- **Database**: SQLite / MySQL
- **Authentication**: Flask-Login, JWT
- **AI Tools**: OpenAI GPT API, TensorFlow.js (Teachable Machine)
- **APIs**: Spoonacular, Open Food Facts
- **DevOps**: GitHub Actions CI, `.env` config handling

---

## ⚙️ Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/TDePalatis/CS467-AI-Coder
    cd CS467-AI-Coder-main
    ```

2. **Install dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Environment Setup**:
    Create a `.env` file (see `.env.example`):
    ```
    FLASK_ENV=development
    SECRET_KEY=your-secret
    JWT_SECRET_KEY=your-jwt-secret
    DATABASE_URL=sqlite:///instance/dev.db
    ```

4. **Run the app**:
    ```bash
    python run.py
    ```

---

## 🌐 Deployment Notes

Supports deployment via:
- Local: Development config with SQLite
- Production: MySQL setup with environment configuration
- Compatible with Google Cloud / Firebase for hosting

---

## ✅ Test Automation (PyTest)

This project includes a suite of automated tests using PyTest and a custom testing configuration.

### Features tested:
- User registration flow
- Duplicate email handling
- Login success and failure
- Protected route access (requires login)

### How to run:
```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt pytest
PYTHONPATH=. python -m pytest -q SmartGroceryApp/tests


---

## 📁 Project Structure

```
SmartGroceryApp/
├── auth/           # Login & register routes
├── grocery_list/   # Smart grocery list views
├── inventory/      # Item tracking & management
├── recipes/        # GPT and API-powered recipes
├── reports/        # Usage data visualization
├── utils/          # GPT helper functions
├── validators/     # JSON schema validation
├── static/         # CSS and model files
├── templates/      # Shared and modular Jinja2 templates
|-- tests           # Test Automation
├── models.py       # SQLAlchemy models
├── config.py       # App configuration by env
└── extensions.py   # Initialized extensions
```

---

## 📊 Reports

Includes usage and spoilage analytics generated via custom logic and visualized through HTML templates and Flask context.

---

## 📄 License

Apache 2.0 License – see [`LICENSE.txt`](./LICENSE.txt)

---

## 🧑‍💻 Authors
Trevor DePalatis, Sayid Ali, Nathan Schuler – Spring 2025

