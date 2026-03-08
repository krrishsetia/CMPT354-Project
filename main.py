import pyodbc

conn = pyodbc.connect(
'driver={ODBC Driver 18 for SQL Server};'
'server=cypress.csil.sfu.ca;'
'uid=s_ksa287;'
'pwd=N3PbfL72nE4nrRdQ;'
'database=ksa287354;'
'TrustServerCertificate=yes;'
)
cursor = conn.cursor()
cursor.execute('SELECT * FROM dbo.yourTable')
for row in cursor:
    print(row)
conn.close()