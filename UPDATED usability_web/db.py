import mysql.connector

def get_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="354p2"
        )
    except Exception as e:
        print("DB error:", e)
        return None