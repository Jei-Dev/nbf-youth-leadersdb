from flask import Blueprint, render_template, request, redirect
from config import get_connection

reg_bp = Blueprint("reg", __name__)

@reg_bp.route("/registration", methods=["GET", "POST"])
def register():

    conn = get_connection()
    cursor = conn.cursor()

    # Load institutions & courses for dropdowns
    cursor.execute("SELECT institution_id, institution_name FROM Institution")
    institutions = cursor.fetchall()

    cursor.execute("SELECT course_id, course_name FROM Course")
    courses = cursor.fetchall()

    error = None  # For duplicate message

    if request.method == "POST":
        # ---------- PERSON DATA ----------
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]

        # Insert Person
        cursor.execute("""
            INSERT INTO Person 
            (first_name, middle_name, last_name, DOB, gender, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (first_name, middle_name, last_name, dob, gender, phone, email))

        conn.commit()

        # Get newly inserted person_id
        cursor.execute("SELECT @@IDENTITY")
        person_id = cursor.fetchone()[0]

        # ---------- ENROLLMENT DATA ----------
        institution_id = request.form["institution_id"]
        course_id = request.form["course_id"]
        enrollment_date = request.form["enrollment_date"]

        # Prevent duplicate enrollment
        cursor.execute("""
            SELECT COUNT(*) FROM Enrollment
            WHERE person_id=? AND institution_id=? AND course_id=?
        """, (person_id, institution_id, course_id))

        if cursor.fetchone()[0] > 0:
            error = "This record already exists!"
        else:
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
                           courses=courses,
                           error=error)
