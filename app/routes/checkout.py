from flask import Blueprint, request, session, redirect, render_template, url_for
from app.models import db, Order, OrderBouquet, CustomerBonus, BonusTransaction, Bouquet
from datetime import datetime
from decimal import Decimal

checkout_bp = Blueprint("checkout", __name__, url_prefix="/checkout")

def get_cart_from_session():
    return session.get("cart", [])

def calculate_totals(cart, bouquet_map, delivery_type):
    subtotal = sum(
        item["quantity"] * bouquet_map[item["bouquet_id"]].bouquet_price
        for item in cart if item["bouquet_id"] in bouquet_map
    )
    discount = round(subtotal * Decimal("0.1")) if delivery_type == "Самовивіз" else 0
    delivery_fee = 150 if delivery_type == "Курєр" and subtotal < 1500 else 0
    total = subtotal - discount + delivery_fee
    return subtotal, discount, delivery_fee, total

@checkout_bp.route("", methods=["POST"], endpoint="checkout")
def checkout():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # Дані з форми
    delivery_type = request.form.get("delivery_type")
    delivery_date = request.form.get("delivery_date")
    delivery_time = request.form.get("delivery_time")
    comment = request.form.get("comment")
    delivery_zone = request.form.get("area")
    delivery_address = request.form.get("address")
    delivery_entrance = request.form.get("entrance")

    # Кошик
    cart = get_cart_from_session()
    bouquet_ids = [item["bouquet_id"] for item in cart]
    bouquets = Bouquet.query.filter(Bouquet.bouquet_id.in_(bouquet_ids)).all()
    bouquet_map = {b.bouquet_id: b for b in bouquets}

    # Розрахунки
    subtotal, discount, delivery_fee, total = calculate_totals(cart, bouquet_map, delivery_type)

    # Зберігаємо замовлення
    new_order = Order(
        customer_id=user_id,
        order_date=datetime.now(),
        subtotal=subtotal,
        discount_amount=discount,
        delivery_fee=delivery_fee,
        total=total,
        delivery_type=delivery_type,
        delivery_zone=delivery_zone,
        delivery_address=delivery_address,
        delivery_entrance=delivery_entrance,
        delivery_date=delivery_date,
        delivery_time=delivery_time,
        comment=comment,
        order_status="Очікує підтвердження"
    )
    db.session.add(new_order)
    db.session.flush()  # щоб отримати order_id

    # Зберігаємо товари
    for item in cart:
        db.session.add(OrderBouquet(
            order_id=new_order.order_id,
            bouquet_id=item["bouquet_id"],
            ordered_quantity=item["quantity"]
        ))

    # Обробка бонусів
    bonus_earned = int(total * 0.05)

    bonus = CustomerBonus.query.filter_by(customer_id=user_id).first()
    if not bonus:
        bonus = CustomerBonus(customer_id=user_id, bonus_points=bonus_earned)
        db.session.add(bonus)
    else:
        bonus.bonus_points += bonus_earned

    db.session.add(BonusTransaction(
        customer_id=user_id,
        change_amount=bonus_earned,
        reason=f"Нарахування за замовлення #{new_order.order_id}"
    ))

    db.session.commit()
    session["cart"] = []
    session["last_order_id"] = new_order.order_id  # для сторінки success

    return redirect(url_for("checkout.success_page"))

@checkout_bp.route("/success", methods=["GET"])
def success_page():
    order_id = session.get("last_order_id")
    if not order_id:
        return redirect("/")

    order = Order.query.get(order_id)
    items = OrderBouquet.query.filter_by(order_id=order_id).all()

    bouquets = [
        {
            "bouquet_name": Bouquet.query.get(item.bouquet_id).bouquet_name,
            "bouquet_price": Bouquet.query.get(item.bouquet_id).bouquet_price,
            "ordered_quantity": item.ordered_quantity
        }
        for item in items
    ]

    bonus = CustomerBonus.query.filter_by(customer_id=order.customer_id).first()

    return render_template("success.html",
                           order=order,
                           bouquets=bouquets,
                           earned_bonus=int(order.total * 0.05),
                           total_bonus=bonus.bonus_points if bonus else 0)