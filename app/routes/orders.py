from flask import Blueprint, request, redirect, render_template, session
from flask import url_for
orders_bp = Blueprint("orders", __name__, url_prefix="/checkout")

@orders_bp.route("", methods=["POST"])
def process_order():
    # Обробка POST-даних форми
    name = request.form.get("name")
    surname = request.form.get("surname")
    phone = request.form.get("phone")
    delivery_type = request.form.get("delivery_type")
    # ... і т.д.

    # TODO: зберегти замовлення до БД

    return redirect(url_for("checkout.success_page"))

