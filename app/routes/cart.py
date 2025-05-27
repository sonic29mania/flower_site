from flask import Blueprint, request, session, jsonify, render_template
from app.extensions import db
from app.models import Bouquet, Customer
import uuid

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


def get_session_id():
    if "cart" not in session:
        session["cart"] = []
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]

def get_cart():
    cart = session.get("cart", [])
    if not isinstance(cart, list) or (cart and not isinstance(cart[0], dict)):
        cart = []
        session["cart"] = []
    return cart


@cart_bp.route("/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    bouquet_id = data.get("bouquet_id")
    is_custom = data.get("is_custom", False)
    flowers = data.get("flowers", [])
    custom_id = data.get("custom_id")
    custom_price = data.get("custom_price")

    cart = get_cart()

    found = False
    for item in cart:
        if is_custom and item.get("is_custom") and item.get("custom_id") == custom_id:
            item["quantity"] += 1
            found = True
            break
        elif not is_custom and item.get("bouquet_id") == bouquet_id:
            item["quantity"] += 1
            found = True
            break

    if not found:
        if is_custom:
            cart.append({
                "is_custom": True,
                "custom_id": custom_id,
                "custom_name": data.get("custom_name"),
                "flowers": flowers,
                "total_price": custom_price,
                "quantity": 1
            })
        else:
            cart.append({
                "is_custom": False,
                "bouquet_id": bouquet_id,
                "quantity": 1
            })

    session["cart"] = cart
    session.modified = True
    return jsonify({"success": True})


@cart_bp.route("/mini")
def mini_cart():
    cart = get_cart()
    bouquet_ids = [item["bouquet_id"] for item in cart if not item.get("is_custom")]
    bouquet_map = {b.bouquet_id: b for b in Bouquet.query.filter(Bouquet.bouquet_id.in_(bouquet_ids)).all()}

    total = 0
    for item in cart:
        if item.get("is_custom"):
            total += item["quantity"] * item.get("total_price", 0)
        else:
            bouquet = bouquet_map.get(item["bouquet_id"])
            if bouquet:
                total += item["quantity"] * bouquet.bouquet_price

    return render_template("mini_cart.html", cart_items=cart, bouquet_map=bouquet_map, total=total)


@cart_bp.route("/")
def cart_page():
    cart = get_cart()
    bouquet_ids = [item["bouquet_id"] for item in cart if not item.get("is_custom")]
    bouquet_map = {b.bouquet_id: b for b in Bouquet.query.filter(Bouquet.bouquet_id.in_(bouquet_ids)).all()}

    subtotal = 0
    for item in cart:
        if item.get("is_custom"):
            subtotal += item["quantity"] * item.get("total_price", 0)
        else:
            bouquet = bouquet_map.get(item["bouquet_id"])
            if bouquet:
                subtotal += item["quantity"] * bouquet.bouquet_price

    delivery_type = request.args.get("delivery_type", "Самовивіз")
    discount = round(subtotal * 0.1) if delivery_type == "Самовивіз" else 0
    delivery_fee = 150 if delivery_type == "Курєр" and subtotal < 1500 else 0
    total = subtotal - discount + delivery_fee

    user = Customer.query.get(session.get("user_id")) if "user_id" in session else None

    return render_template("cart.html", cart_items=cart, bouquet_map=bouquet_map,
                           subtotal=subtotal, discount=discount, delivery_fee=delivery_fee,
                           total=total, delivery_type=delivery_type, user=user)


@cart_bp.route("/update", methods=["POST"])
def update_cart():
    data = request.get_json()
    cart = get_cart()
    action = data.get("action")
    is_custom = data.get("custom") == "true"
    item_id = data.get("bouquet_id")

    for item in cart:
        if is_custom and item.get("is_custom") and item.get("custom_id") == item_id:
            if action == "increase":
                item["quantity"] += 1
            elif action == "decrease":
                item["quantity"] = max(1, item["quantity"] - 1)
            break
        elif not is_custom and not item.get("is_custom") and item["bouquet_id"] == int(item_id):
            if action == "increase":
                item["quantity"] += 1
            elif action == "decrease":
                item["quantity"] = max(1, item["quantity"] - 1)
            break

    session["cart"] = cart
    return _render_cart_update_response()


@cart_bp.route("/remove_item", methods=["POST"])
def remove_item():
    data = request.get_json()
    is_custom = data.get("is_custom", False)
    item_id = data.get("bouquet_id")

    cart = get_cart()
    new_cart = []
    for item in cart:
        if is_custom and item.get("is_custom") and item.get("custom_id") == item_id:
            continue
        elif not is_custom and not item.get("is_custom") and item["bouquet_id"] == int(item_id):
            continue
        new_cart.append(item)

    session["cart"] = new_cart
    return _render_cart_update_response()


@cart_bp.route("/cart_items_block")
def cart_items_block():
    cart = get_cart()
    bouquet_ids = [item["bouquet_id"] for item in cart if not item.get("is_custom")]
    bouquet_map = {b.bouquet_id: b for b in Bouquet.query.filter(Bouquet.bouquet_id.in_(bouquet_ids)).all()}
    return render_template("cart_items_block.html", cart_items=cart, bouquet_map=bouquet_map)



def _render_cart_update_response(delivery_type="Самовивіз"):
    cart = get_cart()
    bouquet_ids = [item["bouquet_id"] for item in cart if not item.get("is_custom")]
    bouquet_map = {b.bouquet_id: b for b in Bouquet.query.filter(Bouquet.bouquet_id.in_(bouquet_ids)).all()}

    subtotal = 0
    for item in cart:
        if item.get("is_custom"):
            subtotal += item["quantity"] * item.get("total_price", 0)
        else:
            bouquet = bouquet_map.get(item["bouquet_id"])
            if bouquet:
                subtotal += item["quantity"] * bouquet.bouquet_price

    # ❗ Знижка лише якщо Самовивіз
    discount = round(subtotal * 0.1) if delivery_type == "Самовивіз" else 0
    delivery_fee = 150 if delivery_type == "Курєр" and subtotal < 1500 else 0
    total = subtotal - discount + delivery_fee

    cart_items_html = render_template("cart_items_block.html", cart_items=cart, bouquet_map=bouquet_map)
    summary_html = render_template("checkout_summary_block.html", subtotal=subtotal, discount=discount,
                                   delivery_fee=delivery_fee, total=total, delivery_type=delivery_type)

    return jsonify(success=True, cart_items_html=cart_items_html, summary_html=summary_html)


@cart_bp.route("/checkout_summary_block")
def checkout_summary_block():
    cart = session.get("cart", [])
    bouquet_ids = [item["bouquet_id"] for item in cart if not item.get("is_custom")]
    bouquet_map = {b.bouquet_id: b for b in Bouquet.query.filter(Bouquet.bouquet_id.in_(bouquet_ids)).all()}

    subtotal = 0
    for item in cart:
        if item.get("is_custom"):
            subtotal += item["quantity"] * item.get("total_price", 0)
        else:
            bouquet = bouquet_map.get(item["bouquet_id"])
            if bouquet:
                subtotal += item["quantity"] * bouquet.bouquet_price

    delivery_type = request.args.get("delivery_type") or "Самовивіз"
    discount = round(subtotal * 0.1) if delivery_type == "Самовивіз" else 0
    delivery_fee = 150 if delivery_type == "Курєр" and subtotal < 1500 else 0
    total = subtotal - discount + delivery_fee

    return render_template("checkout_summary_block.html", subtotal=subtotal, discount=discount,
                           delivery_fee=delivery_fee, total=total, delivery_type=delivery_type)
