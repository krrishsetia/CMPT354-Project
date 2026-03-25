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

# Usage
conn = get_mysql_connection('localhost', 'root', '1925', 'test')

cursor = conn.cursor()
"""
cursor.execute("select * from Part")

rows = cursor.fetchall()

for row in rows:
    print(row)"""
    
    


while True:
    print(f"""
      0. to exit
      1. to print all tables
      2. to print specific table
      3. update table
      
      """)
    user = int(input("what do you want do to: "))
    
    if user == 0:
        conn.close()
        break
    
    if user == 1:
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    
    if user == 2:
        table = input("which table: ")
        cursor.execute(f"""SELECT * 
                           From ? """,table)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    
        
    
    
    