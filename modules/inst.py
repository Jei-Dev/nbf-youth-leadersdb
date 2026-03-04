# inst.py
from flask import Blueprint, render_template, request, redirect, session
from config import get_connection

# ✅ Define the Blueprint first
inst_bp = Blueprint("inst", __name__)

# ✅ Route for /settings
@inst_bp.route("/settings", methods=["GET", "POST"])
def settings():
    if "role" in session:

        # Admin & Staff can access
        if session["role"] in ["Admin", "Staff"]:
            pass

    # 🚫 User cannot access settings
    elif session["role"] == "User":
        return redirect("/registration")
    
    else:
        # Not logged in → redirect to login
        return redirect("/login")

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
        return redirect("/settings")

    # GET request: fetch tables for display
    cursor.execute("SELECT institution_name, inst_short_name FROM Institution")
    institutions = cursor.fetchall()

    cursor.execute("SELECT course_name, course_short_name FROM Course")
    courses = cursor.fetchall()

    conn.close()
    return render_template("settings.html", institutions=institutions, courses=courses)