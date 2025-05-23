from db_config import connect_to_db

def create_blogs_table():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blogs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                slug VARCHAR(100) NOT NULL,
                body TEXT NULL,
                image TEXT NULL,
                status varchar(20) default "active",
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'blogs' created or already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error creating table:", e)

if __name__ == "__main__":
    create_blogs_table()
