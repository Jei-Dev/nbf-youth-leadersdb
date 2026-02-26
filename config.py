import pyodbc
from flask_mail import Mail

def get_connection():
    conn_str = (
        r"Driver={ODBC Driver 18 for SQL Server};"
        r"Server=DESKTOP-P7GIQ5G\SQLEXPRESS02;"
        r"Database=Youth_db;"
        r"Trusted_Connection=yes;"
        r"Encrypt=no;"
    )
    return pyodbc.connect(conn_str)

mail = Mail()

def init_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your_app_password'
    mail.init_app(app)
