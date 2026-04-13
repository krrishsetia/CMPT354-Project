try:
    import mysql.connector
except Exception:
    mysql = None


def get_db():
    if mysql is None:
        print("DB error: mysql-connector-python is not installed.")
        return None

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
