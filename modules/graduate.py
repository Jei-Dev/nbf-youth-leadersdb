from flask import Blueprint, request, redirect, url_for
from config import get_connection

grad_bp = Blueprint("grad", __name__)

@grad_bp.route("/add_graduate", methods=["POST"])
def add_graduate():

    conn = get_connection()
    cursor = conn.cursor()

    enrollment_id = request.form["enrollment_id"]
    graduation_date = request.form["graduation_date"]

    # Check duplicate
    cursor.execute("SELECT COUNT(*) FROM Graduate WHERE enrollment_id=?", (enrollment_id,))
    exists = cursor.fetchone()[0]

    if exists > 0:
        conn.close()
        return redirect(url_for("enrol.enrollment", error="This enrollment is already registered as graduate!"))

    # Insert graduate
    cursor.execute("""
        INSERT INTO Graduate (enrollment_id, graduation_date)
        VALUES (?, ?)
    """, (enrollment_id, graduation_date))

    conn.commit()
    conn.close()

    return redirect("/enrollment")