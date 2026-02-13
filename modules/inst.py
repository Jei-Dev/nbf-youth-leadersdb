from flask import Blueprint, render_template, request, redirect
from config import get_connection

inst_bp = Blueprint("inst", __name__)

@inst_bp.route("/settings", methods=["GET", "POST"])
def settings():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        if "institution_name" in request.form:
            cursor.execute("""
                INSERT INTO Institution (institution_name, inst_short_name)
                VALUES (?, ?)
            """, (
                request.form["institution_name"],
                request.form["inst_short_name"]
            ))

        if "course_name" in request.form:
            cursor.execute("""
                INSERT INTO Course (course_name, course_short_name, duration)
                VALUES (?, ?, ?)
            """, (
                request.form["course_name"],
                request.form["course_short_name"],
                request.form["duration"]
            ))

        conn.commit()
        conn.close()
        return redirect("/settings")

    conn.close()
    return render_template("settings.html")
