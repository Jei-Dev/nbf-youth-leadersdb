from flask import Blueprint, render_template, request, redirect, url_for, session
from config import get_connection, mail
from werkzeug.security import generate_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

reg_bp = Blueprint("reg", __name__)
serializer = URLSafeTimedSerializer("SUPER_SECRET_KEY_CHANGE_THIS")


# ---------------- YOUTH REGISTRATION ----------------
@reg_bp.route("/registration", methods=["GET", "POST"])
def youth_registration():

    from flask import session, redirect

    # 🔐 If logged in:
    if "role" in session:

        # Admin & Staff can access
        if session["role"] in ["Admin", "Staff"]:
            pass

        # User can access (this is their only page)
        elif session["role"] == "User":
            pass
    else:
        # Not logged in → redirect to login
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT institution_id, institution_name FROM Institution")
    institutions = cursor.fetchall()

    cursor.execute("SELECT course_id, course_name FROM Course")
    courses = cursor.fetchall()

    if request.method == "POST":

        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]

        cursor.execute("""
            INSERT INTO Person
            (first_name, middle_name, last_name, DOB, gender, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (first_name, middle_name, last_name, dob, gender, phone, email))

        conn.commit()
        cursor.execute("SELECT @@IDENTITY")
        person_id = cursor.fetchone()[0]

        institution_id = request.form["institution_id"]
        course_id = request.form["course_id"]
        enrollment_date = request.form["enrollment_date"]

        cursor.execute("""
            INSERT INTO Enrollment
            (person_id, institution_id, course_id, enrollment_date)
            VALUES (?, ?, ?, ?)
        """, (person_id, institution_id, course_id, enrollment_date))

        conn.commit()
        conn.close()
        return redirect("/registration")

    conn.close()
    return render_template("registration.html",
                           institutions=institutions,
                           courses=courses)


# ---------------- USER REGISTRATION (MODAL) ----------------
@reg_bp.route("/register", methods=["POST"])
def register_user():

    conn = get_connection()
    cursor = conn.cursor()

    person_id = request.form["person_id"]
    username = request.form["username"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])
    role = request.form["role"]

    token = serializer.dumps(email, salt="email-confirm")

    cursor.execute("""
        INSERT INTO Users
        (person_id, username, password_hash, email, role, verification_token)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (person_id, username, password, email, role, token))

    conn.commit()
    conn.close()

    msg = Message("Verify Your Account",
                  sender="your_email@gmail.com",
                  recipients=[email])

    link = url_for("reg.verify_email", token=token, _external=True)
    msg.body = f"Click to verify account: {link}"
    mail.send(msg)

    return redirect("/login")


@reg_bp.route("/verify/<token>")
def verify_email(token):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        email = serializer.loads(token, salt="email-confirm", max_age=3600)
    except:
        return "Invalid or expired link."

    cursor.execute("UPDATE Users SET is_verified=1 WHERE email=?", (email,))
    conn.commit()
    conn.close()

    return redirect("/login")

# ---------------- USER MANAGEMENT (ADMIN ONLY) ----------------
@reg_bp.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    # 🔐 Admin Protection
    if "role" not in session or session["role"] != "Admin":
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        action = request.form.get("action")

        # CREATE USER
        if action == "create":
            person_id = request.form["person_id"]
            username = request.form["username"]
            email = request.form["email"]
            role = request.form["role"]
            password = generate_password_hash(request.form["password"])

            cursor.execute("""
                INSERT INTO Users
                (person_id, username, password_hash, email, role)
                VALUES (?, ?, ?, ?, ?)
            """, (person_id, username, password, email, role))
            conn.commit()

    # LOAD DATA
    cursor.execute("""
        SELECT DISTINCT p.person_id,
               p.first_name + ' ' + p.last_name
        FROM Person p
        INNER JOIN Enrollment e ON p.person_id = e.person_id
        WHERE p.person_id NOT IN (SELECT person_id FROM Users)
    """)
    persons = cursor.fetchall()

    cursor.execute("""
        SELECT u.user_id,
               p.first_name + ' ' + p.last_name AS person_name,
               u.username,
               u.email,
               u.role,
               u.is_verified
        FROM Users u
        INNER JOIN Person p ON u.person_id = p.person_id
        ORDER BY u.user_id DESC
    """)
    users = cursor.fetchall()

    conn.close()

    return render_template("manage_users.html",
                           persons=persons,
                           users=users)


# ---------------- DELETE USER ----------------
@reg_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
        conn.commit()
        return '', 200
    except Exception as e:
        print(e)
        return '', 500
    finally:
        conn.close()

    # Existing users
    cursor.execute("""
        SELECT u.user_id,
               p.first_name + ' ' + p.last_name,
               u.username,
               u.email,
               u.role,
               u.is_verified
        FROM Users u
        INNER JOIN Person p ON u.person_id = p.person_id
        ORDER BY u.user_id DESC
    """)
    users = cursor.fetchall()

    conn.close()

    return render_template("manage_users.html",
                           persons=persons,
                           users=users)

