from flask import Blueprint, render_template, request, redirect
from config import get_connection

grad_bp = Blueprint("grad", __name__)

# Route to add a graduate
@grad_bp.route("/add_graduate", methods=["GET", "POST"])
def add_graduate():
    conn = get_connection()
    cursor = conn.cursor()

    # Get enrollments not yet graduated
    cursor.execute("""
        SELECT e.enrollment_id,
               p.first_name + ' ' + p.last_name AS person_name,
               i.institution_id, i.institution_name, i.inst_short_name,
               c.course_id, c.course_name, c.course_short_name
        FROM Enrollment e
        INNER JOIN Person p ON e.person_id = p.person_id
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        INNER JOIN Course c ON e.course_id = c.course_id
        WHERE e.enrollment_id NOT IN (SELECT enrollment_id FROM Graduate)
    """)
    enrollments = cursor.fetchall()

    error = None

    if request.method == "POST":
        enrollment_id = request.form["enrollment_id"]
        graduation_date = request.form["graduation_date"]

        # Prevent duplicate
        cursor.execute("SELECT COUNT(*) FROM Graduate WHERE enrollment_id=?", (enrollment_id,))
        if cursor.fetchone()[0] > 0:
            error = "This enrollment is already registered as graduate!"
        else:
            cursor.execute("""
                INSERT INTO Graduate (enrollment_id, graduation_date)
                VALUES (?, ?)
            """, (enrollment_id, graduation_date))
            conn.commit()
            conn.close()
            return redirect("/view_graduates")

    conn.close()
    return render_template("add_graduate.html", enrollments=enrollments, error=error)


# Route to view graduates
@grad_bp.route("/view_graduates")
def view_graduates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.graduate_id,
               p.first_name + ' ' + p.last_name AS person_name,
               i.inst_short_name, 
               c.course_short_name,
               i.institution_name,
               c.course_name,
               g.graduation_date
        FROM Graduate g
        INNER JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
        INNER JOIN Person p ON e.person_id = p.person_id
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        INNER JOIN Course c ON e.course_id = c.course_id
        ORDER BY g.graduate_id DESC
    """)
    graduates = cursor.fetchall()
    conn.close()

    # Add unique_number for each graduate
    graduates_with_number = []
    for grad in graduates:
        grad_id = grad[0]
        person_name = grad[1]
        inst_short = grad[2]
        course_short = grad[3]
        inst_name = grad[4]
        course_name = grad[5]
        grad_date = grad[6]
        unique_number = f"NBF|{inst_short}{grad_date.year % 100:02d}|{course_short}{grad_id:03d}"
        graduates_with_number.append({
            "graduate_id": grad_id,
            "person_name": person_name,
            "institution_name": inst_name,
            "course_name": course_name,
            "graduation_date": grad_date,
            "unique_number": unique_number
        })

    return render_template("view_graduates.html", graduates=graduates_with_number)
