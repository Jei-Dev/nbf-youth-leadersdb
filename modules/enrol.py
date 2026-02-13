from flask import Blueprint, render_template, request, redirect
from config import get_connection
from datetime import date

enrol_bp = Blueprint("enrol", __name__)

@enrol_bp.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    conn = get_connection()
    cursor = conn.cursor()

    # Load dropdown data
    cursor.execute("SELECT person_id, first_name, last_name FROM Person")
    persons = cursor.fetchall()

    cursor.execute("SELECT institution_id, institution_name, inst_short_name FROM Institution")
    institutions = cursor.fetchall()

    cursor.execute("SELECT course_id, course_name, course_short_name FROM Course")
    courses = cursor.fetchall()

    error = None  # for duplicate message

    # -------- INSERT ENROLLMENT --------
    if request.method == "POST" and "add_enrollment" in request.form:
        person_id = request.form["person_id"]
        institution_id = request.form["institution_id"]
        course_id = request.form["course_id"]
        enrollment_date = request.form["enrollment_date"]

        # Prevent duplicate
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
            return redirect("/enrollment")

    # -------- DELETE ENROLLMENT --------
    if request.method == "POST" and "delete_id" in request.form:
        cursor.execute("DELETE FROM Enrollment WHERE enrollment_id=?", (request.form["delete_id"],))
        conn.commit()
        return redirect("/enrollment")

    # -------- UPDATE ENROLLMENT --------
    if request.method == "POST" and "edit_id" in request.form:
        cursor.execute("""
            UPDATE Enrollment
            SET institution_id=?, course_id=?, enrollment_date=?
            WHERE enrollment_id=?
        """, (
            request.form["institution_id"],
            request.form["course_id"],
            request.form["enrollment_date"],
            request.form["edit_id"]
        ))
        conn.commit()
        return redirect("/enrollment")

    # -------- MARK AS GRADUATE --------
    if request.method == "POST" and "graduate_id" in request.form:
        enrollment_id = request.form["graduate_id"]
        grad_date = request.form.get("graduation_date", date.today())

        # Prevent duplicate in Graduate table
        cursor.execute("SELECT COUNT(*) FROM Graduate WHERE enrollment_id=?", (enrollment_id,))
        if cursor.fetchone()[0] > 0:
            error = "This enrollment is already a graduate!"
        else:
            # Insert into Graduate table (do NOT insert graduate_id)
            cursor.execute("INSERT INTO Graduate (enrollment_id, graduation_date) VALUES (?, ?)",
                           (enrollment_id, grad_date))
            conn.commit()
            return redirect("/enrollment")

    # -------- VIEW ENROLLMENTS WITH INNER JOIN --------
    cursor.execute("""
        SELECT 
            e.enrollment_id,
            p.first_name + ' ' + p.last_name AS person_name,
            i.institution_name,
            i.inst_short_name,
            c.course_name,
            c.course_short_name,
            e.enrollment_date
        FROM Enrollment e
        INNER JOIN Person p ON e.person_id = p.person_id
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        INNER JOIN Course c ON e.course_id = c.course_id
        ORDER BY e.enrollment_id DESC
    """)
    records = cursor.fetchall()
    conn.close()

    return render_template("enrollment.html",
                           persons=persons,
                           institutions=institutions,
                           courses=courses,
                           records=records,
                           error=error)
