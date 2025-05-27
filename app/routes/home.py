
from flask import Blueprint, render_template
from app.models import Bouquet, OrderBouquet, Order
from sqlalchemy import func

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    # Найпопулярніші букети за кількістю замовлень
    subquery = (
        OrderBouquet.query
        .join(Order, OrderBouquet.order_id == Order.order_id)
        .filter(Order.order_status == "Завершено")
        .with_entities(
            OrderBouquet.bouquet_id,
            func.sum(OrderBouquet.ordered_quantity).label("total_sold")
        )
        .group_by(OrderBouquet.bouquet_id)
        .subquery()
    )

    bouquets = (
        Bouquet.query
        .join(subquery, Bouquet.bouquet_id == subquery.c.bouquet_id)
        .add_columns(
            Bouquet.bouquet_id,
            Bouquet.bouquet_name,
            Bouquet.bouquet_price,
            Bouquet.bouquet_image,
            subquery.c.total_sold
        )
        .order_by(subquery.c.total_sold.desc())
        .limit(12)
        .all()
    )

    result = [
        {
            "bouquet_id": b.bouquet_id,
            "bouquet_name": b.bouquet_name,
            "bouquet_price": b.bouquet_price,
            "bouquet_image": b.bouquet_image,
            "total_sold": b.total_sold
        }
        for b in bouquets
    ]

    return render_template("home.html", bouquets=result)
