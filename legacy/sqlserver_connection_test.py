"""Legacy SQL Server connection test kept for team reference.

Important: move credentials to environment variables before using this in a shared repo.
"""
import os
import pyodbc

conn = pyodbc.connect(
    'driver={ODBC Driver 18 for SQL Server};'
    f"server={os.getenv('CMPT354_SQL_SERVER', 'cypress.csil.sfu.ca')};"
    f"uid={os.getenv('CMPT354_SQL_USER', '')};"
    f"pwd={os.getenv('CMPT354_SQL_PASSWORD', '')};"
    f"database={os.getenv('CMPT354_SQL_DATABASE', '')};"
    'TrustServerCertificate=yes;'
)

cursor = conn.cursor()
cursor.execute('SELECT TOP 5 name FROM sys.tables')
for row in cursor:
    print(row)
conn.close()
