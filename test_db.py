import pyodbc

conn_str = (
    r"Driver={ODBC Driver 18 for SQL Server};"
    r"Server=DESKTOP-P7GIQ5G\SQLEXPRESS02;"
    r"Database=Youth_db;"
    r"Trusted_Connection=yes;"
    r"Encrypt=no;"           # <-- add this line
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("✅ Connection successful")
except Exception as e:
    print("❌ Connection failed")
    print(e)
