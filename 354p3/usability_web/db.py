import pyodbc
def get_mysql_connection(host, user, password, database):
    drivers = [d for d in pyodbc.drivers() if 'MySQL' in d]
    if not drivers:
        raise Exception("No MySQL ODBC Driver found. Please install the MySQL Connector.")
    
    driver = drivers[0] 
    
    # 2. Build the connection string
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"USER={user};"
        f"PASSWORD={password};"
        f"OPTION=3;" # Option 3 enables dynamic cursors
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        print(f"Successfully connected to {database} using {driver}")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None