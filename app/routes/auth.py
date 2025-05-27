# === auth.py ===
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.utils.email_utils import send_code_to_email
import random
import mysql.connector
import time

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_db_connection():
    return mysql.connector.connect(**db)

def generate_code():
    return str(random.randint(10000, 99999))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    session.pop("verify_code", None)
    session.pop("login_email", None)
    session.pop("user_id", None)

    if request.method == "POST":
        email = request.form.get("email")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE customer_email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return render_template("login.html", error="Користувача з таким email не знайдено")

        code = generate_code()
        session["verify_code"] = code
        session["login_email"] = email
        session["code_timestamp"] = time.time()

        send_code_to_email(email, code)
        flash("Код підтвердження надіслано на пошту.")

        return redirect(url_for("auth.verify"))

    return render_template("login.html")

@auth_bp.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        input_code = request.form.get("code")
        real_code = session.get("verify_code")
        email = session.get("login_email")
        code_time = session.get("code_timestamp")

        if not real_code or not code_time or time.time() - code_time > 180:
            flash("Код підтвердження прострочено. Спробуйте знову.")
            return redirect(url_for("auth.login"))

        if input_code == real_code:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customer WHERE customer_email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session["user_id"] = user["customer_id"]
                session.pop("verify_code", None)
                session.pop("login_email", None)
                session.pop("code_timestamp", None)
                return redirect(url_for("profile.profile"))

        return render_template("verify_code.html", error="Невірний код")

    return render_template("verify_code.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Ви вийшли з акаунту.")
    return redirect(url_for("auth.login"))

