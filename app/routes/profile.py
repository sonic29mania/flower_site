from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.models import Customer, Order, OrderBouquet, Bouquet
from app.extensions import db


profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))  # auth буде пізніше

    user = Customer.query.get(user_id)

    if request.method == "POST":
        user.customer_name = request.form.get("name")
        user.customer_surname = request.form.get("surname")
        user.customer_email = request.form.get("customer_email")
        user.customer_steet_and_number = request.form.get("address")
        user.customer_phone = request.form.get("phone")
        db.session.commit()
        flash("Профіль оновлено успішно.")

    required_fields = ["customer_surname", "customer_name", "customer_email", "customer_phone"]
    missing_fields = [field for field in required_fields if not getattr(user, field)]

    # Історія замовлень
    orders = Order.query.filter_by(customer_id=user_id, order_status='Завершено').all()
    order_history = []
    for order in orders:
        for item in order.bouquets:
            bouquet = Bouquet.query.get(item.bouquet_id)
            order_history.append({
                "bouquet_id": bouquet.bouquet_id,
                "bouquet_name": bouquet.bouquet_name,
                "bouquet_price": bouquet.bouquet_price,
                "bouquet_image": bouquet.bouquet_image,
                "ordered_quantity": item.ordered_quantity
            })

    return render_template("client_profile.html", user=user, missing_fields=missing_fields, order_history=order_history)
