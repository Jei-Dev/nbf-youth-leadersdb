from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from config import get_connection, mail
import datetime

auth_bp = Blueprint("auth", __name__)
serializer = URLSafeTimedSerializer("SUPER_SECRET_KEY_CHANGE_THIS")

# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    conn = get_connection()
    cursor = conn.cursor()

    # ================= BOOTSTRAP FIRST ADMIN =================
    cursor.execute("SELECT COUNT(*) FROM Users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        conn.close()
        return redirect("/setup_admin")  # redirect to setup first admin

    # ---------------- LOGIN PROCESS ----------------
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("""
            SELECT user_id, password_hash, is_verified, role
            FROM Users WHERE username=?
        """, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            if user[2] == 0:
                conn.close()
                return "Please verify your email first."

            session["user_id"] = user[0]
            session["role"] = user[3]
            conn.close()
            return redirect("/dashboard")

        conn.close()
        return "Invalid credentials"

    conn.close()
    return render_template("login.html")


# ---------------- SETUP FIRST ADMIN ----------------
@auth_bp.route("/setup_admin", methods=["GET", "POST"])
def setup_admin():
    conn = get_connection()
    cursor = conn.cursor()

    # Safety check: block if Users already exist
    cursor.execute("SELECT COUNT(*) FROM Users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect("/login")

    # Only allow persons who are enrolled
    cursor.execute("""
        SELECT DISTINCT p.person_id,
               p.first_name + ' ' + p.last_name
        FROM Person p
        INNER JOIN Enrollment e ON p.person_id = e.person_id
    """)
    persons = cursor.fetchall()

    if request.method == "POST":
        person_id = request.form["person_id"]
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        cursor.execute("""
            INSERT INTO Users
            (person_id, username, password_hash, email, role, is_verified)
            VALUES (?, ?, ?, ?, 'Admin', 1)
        """, (person_id, username, password, email))

        conn.commit()
        conn.close()
        return redirect("/login")

    conn.close()
    return render_template("setup_admin.html", persons=persons)


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route("/forgot_password", methods=["POST"])
def forgot_password():
    conn = get_connection()
    cursor = conn.cursor()

    email = request.form["email"]
    token = serializer.dumps(email, salt="reset-password")
    expiry = datetime.datetime.now() + datetime.timedelta(hours=1)

    cursor.execute("""
        UPDATE Users SET reset_token=?, token_expiry=? WHERE email=?
    """, (token, expiry, email))
    conn.commit()
    conn.close()

    msg = Message("Reset Password",
                  sender="your_email@gmail.com",
                  recipients=[email])

    link = url_for("auth.reset_password", token=token, _external=True)
    msg.body = f"Click to reset password: {link}"
    mail.send(msg)

    return redirect("/login")


# ---------------- RESET PASSWORD ----------------
@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        email = serializer.loads(token, salt="reset-password", max_age=3600)
    except:
        conn.close()
        return "Token expired or invalid."

    if request.method == "POST":
        new_password = generate_password_hash(request.form["password"])

        cursor.execute("""
            UPDATE Users SET password_hash=?, reset_token=NULL, token_expiry=NULL
            WHERE email=?
        """, (new_password, email))
        conn.commit()
        conn.close()
        return redirect("/login")

    conn.close()
    return render_template("reset_password.html")