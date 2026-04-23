import os
import psycopg2

os.environ['PGPASSWORD'] = 'Zhang123'

try:
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='postgres',
        user='postgres',
        password='Zhang123'
    )
    print("Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='welcome_assistant'")
    result = cursor.fetchone()
    
    if not result:
        cursor.execute("CREATE DATABASE welcome_assistant")
        print("Database welcome_assistant created!")
    else:
        print("Database welcome_assistant already exists")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
