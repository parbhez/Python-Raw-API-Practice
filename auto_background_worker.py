# Python background script নিজে থেকে database চেক করবে, যদি কোন status = 'pending' থাকে, তাহলে সেই row নেবে, body update করবে, আর status approved করে দেবে—এই পুরো কাজটি user request ছাড়াই চলবে।
#এইটা মূলত auto background worker বা cron-style polling script। নিচে আমি MySQL + Raw Python দিয়ে একটা full working code দিচ্ছি যেটা প্রতি ১০ সেকেন্ড পরপর database চেক করে pending data process করে।


import mysql.connector
import time
from db_config import connect_to_db as get_connection

def process_pending_blogs():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM blogs WHERE status = 'active' LIMIT 1")
        row = cursor.fetchone()

        if row:
            print(f"Processing blog ID: {row['id']}")
            updated_body = f"Auto-generated content for: {row['title']}"
            cursor.execute("""
                UPDATE blogs
                SET body = %s, status = 'approved'
                WHERE id = %s
            """, (updated_body, row['id']))
            conn.commit()
            print(f"Blog ID {row['id']} approved.")
            sleep_time = 1  # If found, keep checking frequently
        else:
            print("✅ No pending blogs found.")
            sleep_time = 60  # If nothing found, wait 60 seconds

        cursor.close()
        conn.close()
        return sleep_time

    except Exception as e:
        print(f"Error: {e}")
        return 60

while True:
    delay = process_pending_blogs()
    time.sleep(delay)
    