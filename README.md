# Python Blog API and Background Worker

This project includes:
- A simple **Blog CRUD API** using raw Python and MySQL.
- An **Auto Background Worker** that processes pending blog entries and updates their status automatically.
- A **Server Launcher Script** that starts all necessary Python scripts together (for production or dev use).

---

## 📁 Project Structure

├── .env # Database connection setup
├── create_database.py # create Database
├── create_blogs_table.py # create blogs table
├── db_config.py # MySQL connection settings
├── blog_api.py # Blog CRUD API (Raw Python, no framework)
├── auto_background_worker.py # Background script to process pending blog items
├── multiple_run_development_server.py # Starts all required scripts together in development server
├── multiple_run_production_server.py # Starts all required scripts together in production server
└── README.md # Project documentation



---

## 🧠 Features

### ✅ blog_api.py
- Serves as a basic web API for blog CRUD (Create, Read, Update, Delete).
- Uses Python `http.server` module.
- Connects to MySQL directly (no ORM used).

### ✅ auto_background_worker.py
- Every 10 seconds, checks the database for blogs with `status = 'active'`.
- If found, generates content in the `body` and updates `status = 'approved'`.
- Runs continuously in background like a daemon/worker.

### ✅ multiple_run_production_server.py
- Watches file changes (only for development).
- Can be modified for production to run both `blog_api.py` and `auto_background_worker.py` without auto-reload.

---

## ⚙️ How to Run (Development)

1. **Install Dependencies:**

```bash
pip install mysql-connector-python watchdog


---

## 🔧 Run Production Server

Run both the API and background worker together using:

```bash
python multiple_run_production_server.py
