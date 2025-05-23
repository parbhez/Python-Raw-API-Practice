from db_config import connect_to_server, DB_NAME

def create_database():
    try:
        conn = connect_to_server()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' created or already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error creating database:", e)

if __name__ == "__main__":
    create_database()