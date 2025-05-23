# Python Blog API and Background Worker

This project includes:
- A simple **Blog CRUD API** using raw Python and MySQL.
- An **Auto Background Worker** that processes pending blog entries and updates their status automatically.
- A **Server Launcher Script** that starts all necessary Python scripts together (for production or dev use).

---

## 📁 Project Structure

📁 Project Root/
│
├── 📄 .env  
│   🔹 Environment variables (e.g., DB_HOST, DB_USER, DB_PASS, DB_NAME)
│
├── 📄 create_database.py  
│   🔹 Script to create MySQL database if not exists
│
├── 📄 create_blogs_table.py  
│   🔹 Script to create the `blogs` table inside the database
│
├── 📄 db_config.py  
│   🔹 Centralized MySQL connection configuration using `mysql.connector`
│
├── 📄 blog_api.py  
│   🔹 Blog CRUD API using only raw Python and built-in HTTPServer (no framework)
│   🔹 Accessible at: [http://localhost:800](http://localhost:800)
│
├── 📄 auto_background_worker.py  
│   🔹 Background worker script that checks for pending blog items and processes them automatically
│   🔹 No user interaction needed
│
├── 📄 multiple_run_development_server.py  
│   🔹 Starts both `blog_api.py` and `auto_background_worker.py` with auto-reload on file changes
│   🔸 🚫 Not suitable for production
│
├── 📄 multiple_run_production_server.py  
│   🔹 Starts both `blog_api.py` and `auto_background_worker.py` without reload (production ready)
│   🔹 Keeps processes alive until terminated
│
└── 📄 README.md  
    🔹 Full project usage guide, setup instructions, and run commands




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
