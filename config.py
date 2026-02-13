import pyodbc

def get_connection():
    conn_str = (
        r"Driver={ODBC Driver 18 for SQL Server};"
        r"Server=DESKTOP-P7GIQ5G\SQLEXPRESS02;"
        r"Database=Youth_db;"
        r"Trusted_Connection=yes;"
        r"Encrypt=no;"
    )
    return pyodbc.connect(conn_str)
