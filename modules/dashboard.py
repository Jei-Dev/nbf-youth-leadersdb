# modules/dashboard.py
from flask import Blueprint, jsonify, render_template
from config import get_connection
from datetime import date

dash_bp = Blueprint("dash", __name__)

# ---------------- DASHBOARD PAGE ----------------
@dash_bp.route("/dashboard")
def dashboard():
    """
    Serve the dashboard page with summary stats.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total enrollments
    cursor.execute("SELECT COUNT(*) FROM Enrollment")
    total_enrollments = cursor.fetchone()[0]

    # Total graduates
    cursor.execute("SELECT COUNT(*) FROM Graduate")
    total_graduates = cursor.fetchone()[0]

    # Pending graduates (enrollments not yet in Graduate table)
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Enrollment e
        LEFT JOIN Graduate g ON e.enrollment_id = g.enrollment_id
        WHERE g.enrollment_id IS NULL
    """)
    pending_graduates = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_enrollments=total_enrollments,
        total_graduates=total_graduates,
        pending_graduates=pending_graduates
    )


# ---------------- API TO GET GRADUATES ----------------
@dash_bp.route("/api/graduates")
def api_graduates():
    """
    Returns a JSON list of graduates with calculated Graduate ID.
    Format: NBF|<institution_short><YY>|<course_short><3-digit enrollment number>
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all fields needed for display and calculation
    cursor.execute("""
        SELECT g.enrollment_id, g.graduation_date,
               p.first_name + ' ' + p.last_name AS person_name,
               i.inst_short_name,
               i.institution_name,
               c.course_short_name,
               c.course_name,
               c.course_id,
               i.institution_id
        FROM Graduate g
        INNER JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
        INNER JOIN Person p ON e.person_id = p.person_id
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        INNER JOIN Course c ON e.course_id = c.course_id
        ORDER BY i.institution_id, c.course_id, g.graduation_date
    """)
    rows = cursor.fetchall()
    conn.close()

    # Track counts per course per institution per graduation year
    course_counts = {}
    graduates = []

    for row in rows:
        enrollment_id_db = row[0]
        grad_date = row[1]
        person_name = row[2]
        inst_short = row[3] or ""
        inst_name = row[4] or ""
        course_short = row[5] or ""
        course_name = row[6] or ""
        course_id = row[7]
        institution_id = row[8]

        # Key for counting: institution + course + year
        key = (institution_id, course_id, grad_date.year)
        course_counts[key] = course_counts.get(key, 0) + 1
        count = course_counts[key]

        # Build graduate_id dynamically: NBF|INSTYY|COURSE### (e.g., NBF|ABC24|MG001)
        graduate_id = f"NBF|{inst_short}{str(grad_date.year)[-2:]}|{course_short}{str(count).zfill(3)}"

        graduates.append({
            "graduate_id": graduate_id,
            "name": person_name,
            "institution_name": inst_name,
            "institution_short": inst_short,
            "course_name": course_name,
            "course_short": course_short,
            "graduation_date": grad_date.strftime("%Y-%m-%d")
        })

    return jsonify(graduates)

@dash_bp.route("/api/enrollments")
def api_enrollments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.enrollment_id,
               p.first_name + ' ' + p.last_name,
               i.inst_short_name,
               c.course_short_name,
               CASE 
                   WHEN g.enrollment_id IS NOT NULL THEN 'Graduated'
                   ELSE 'Active'
               END AS status
        FROM Enrollment e
        INNER JOIN Person p ON e.person_id = p.person_id
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        INNER JOIN Course c ON e.course_id = c.course_id
        LEFT JOIN Graduate g ON e.enrollment_id = g.enrollment_id
    """)

    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "enrollment_id": r[0],
            "name": r[1],
            "institution_short": r[2],
            "course_short": r[3],
            "status": r[4]
        })

    return jsonify(data)

@dash_bp.route("/api/users")
def api_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.first_name + ' ' + p.last_name,
               u.username,
               u.role
        FROM Users u
        INNER JOIN Person p ON u.person_id = p.person_id
    """)

    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "username": r[1],
            "role": r[2]
        })

    return jsonify(data)

#==========Charts section===============
@dash_bp.route("/api/chart/institution")
def chart_institution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.inst_short_name, COUNT(*)
        FROM Graduate g
        INNER JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        GROUP BY i.inst_short_name
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "labels": [r[0] for r in rows],
        "values": [r[1] for r in rows]
    })


# graduates per course per year
@dash_bp.route("/api/chart/course_year")
def chart_course_year():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.course_short_name,
               YEAR(g.graduation_date),
               COUNT(*)
        FROM Graduate g
        INNER JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
        INNER JOIN Course c ON e.course_id = c.course_id
        GROUP BY c.course_short_name, YEAR(g.graduation_date)
        ORDER BY YEAR(g.graduation_date)
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)

@dash_bp.route("/api/chart/enrollments_per_institution")
def chart_enrollments_per_institution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.inst_short_name, COUNT(*)
        FROM Enrollment e
        INNER JOIN Institution i ON e.institution_id = i.institution_id
        GROUP BY i.inst_short_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify({
        "labels": [r[0] for r in rows],
        "values": [r[1] for r in rows]
    })