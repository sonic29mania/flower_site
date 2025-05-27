from app.extensions import db


from flask import Blueprint, render_template, request
from app.models import FlowerDetails, Color, Size, TypeOfFlower, Ribbon, Packaging
import math

constructor_bp = Blueprint("constructor", __name__)

@constructor_bp.route("/constructor")
def constructor():
    page = request.args.get("page", 1, type=int)
    per_page = 21
    offset = (page - 1) * per_page

    selected_color_ids = request.args.getlist("color", type=int)
    selected_size_ids = request.args.getlist("size", type=int)
    selected_type_ids = request.args.getlist("type", type=int)

    # Всі фільтри
    colors = Color.query.all()
    sizes = Size.query.all()
    types = TypeOfFlower.query.all()
    ribbons = Ribbon.query.all()
    packaging = Packaging.query.all()

    # Запит квітів
    query = FlowerDetails.query.filter(FlowerDetails.flower_image.isnot(None))

    if selected_color_ids:
        query = query.filter(FlowerDetails.color_id.in_(selected_color_ids))
    if selected_size_ids:
        query = query.filter(FlowerDetails.size_id.in_(selected_size_ids))
    if selected_type_ids:
        query = query.join(FlowerDetails, FlowerDetails.flower_id == FlowerDetails.flower_id)
        query = query.join("flower").filter_by(type_f_id=selected_type_ids[0])  # простий фільтр за першим

    all_flowers = query.all()
    total = len(all_flowers)
    flowers = all_flowers[offset:offset + per_page]
    total_pages = math.ceil(total / per_page)

    return render_template("constructor.html",
                           flowers=flowers,
                           ribbons=ribbons,
                           packaging=packaging,
                           colors=colors,
                           sizes=sizes,
                           types=types,
                           selected_color_ids=selected_color_ids,
                           selected_size_ids=selected_size_ids,
                           selected_type_ids=selected_type_ids,
                           current_page=page,
                           total_pages=total_pages)