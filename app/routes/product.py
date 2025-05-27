from flask import Blueprint, render_template, request
from app.models.bouquet import Bouquet
from app.models.bouquet_set import BouquetSet
from app.models.flower import Flower
from app.models.color import Color
from app.models.size import Size
from app.models.type_b import TypeB
from app.models.occasion import Occasion
from app.models.whom import Whom
from app.models.bouquet_1 import BouquetMeta
from sqlalchemy import func, or_, cast, Integer
from sqlalchemy.orm import aliased
from app.extensions import db
import logging

product_bp = Blueprint('product', __name__)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@product_bp.route('/product/<int:bouquet_id>')
def product(bouquet_id):
    filters = {
        'occasion_id': request.args.get("occasion", type=int),
        'color_id': request.args.get("color", type=int),
        'size_id': request.args.get("size", type=int),
        'type_b_id': request.args.get("type", type=int),
        'whom_id': request.args.get("whom", type=int)
    }
    # Прибираємо None
    filters = {k: v for k, v in filters.items() if v is not None}

    bouquet = get_bouquet_by_id(bouquet_id)
    if not bouquet:
        return render_template("404.html"), 404

    similar = get_similar_bouquets(bouquet_id, filters)
    logger.info(f"Similar bouquets for bouquet_id {bouquet_id}: {len(similar)}")
    return render_template("product.html", bouquet=bouquet, similar=similar)

def get_bouquet_by_id(bouquet_id):
    ColorFlower = aliased(Color, name='color_flower')  # Alias for flower color
    bouquet = (
        db.session.query(Bouquet)
        .outerjoin(Size, Bouquet.size_id == Size.size_id)
        # Removed .outerjoin(Color, Bouquet.color_id == Color.color_id) since color_id is missing
        .outerjoin(BouquetMeta, Bouquet.bouquet_id == BouquetMeta.bouquet_id)
        .outerjoin(TypeB, BouquetMeta.type_b_id == TypeB.type_b_id)
        .outerjoin(BouquetSet, Bouquet.bouquet_id == BouquetSet.bouquet_id)
        .outerjoin(Flower, BouquetSet.flower_id == Flower.flower_id)
        .outerjoin(ColorFlower, BouquetSet.flower_color_id == ColorFlower.color_id)
        .filter(Bouquet.bouquet_id == bouquet_id)
        .group_by(
            Bouquet.bouquet_id,
            Bouquet.bouquet_name,
            Bouquet.bouquet_price,
            Bouquet.bouquet_obviousness,
            Bouquet.bouquet_image,
            Size.size_name,
            # Removed Color.color_name from group_by
        )
        .with_entities(
            Bouquet.bouquet_id,
            Bouquet.bouquet_name,
            Bouquet.bouquet_price,
            Bouquet.bouquet_obviousness,
            Bouquet.bouquet_image,
            Size.size_name,
            # Removed Color.color_name.label('color_name'),
            func.max(TypeB.type_b_name).label('type_b_name'),
            func.max(BouquetMeta.type_b_id).label('type_b_id'),
            func.group_concat(
                func.concat(
                    Flower.flower_name, ' (', ColorFlower.color_name, ') ×', BouquetSet.quantity
                ).distinct()
            ).label('bouquet_content')
        )
        .first()
    )
    return bouquet._asdict() if bouquet else None

def get_similar_bouquets(bouquet_id, filters):
    bouquet = Bouquet.query.get(bouquet_id)
    bouquet_meta = BouquetMeta.query.filter_by(bouquet_id=bouquet_id).first()
    if not bouquet:
        return []

    flower_ids = [bs.flower_id for bs in BouquetSet.query.filter_by(bouquet_id=bouquet_id).all()]
    Meta = aliased(BouquetMeta)

    flower_score = func.count(
        func.if_(BouquetSet.flower_id.in_(flower_ids), 1, None)
    ).label("flower_score")

    match_score = (
        cast(Bouquet.size_id == (bouquet.size_id if bouquet.size_id else None), Integer) +
        cast(Meta.occasion_id == (bouquet_meta.occasion_id if bouquet_meta else None), Integer) * 2 +
        cast(Meta.whom_id == (bouquet_meta.whom_id if bouquet_meta else None), Integer) +
        cast(Meta.type_b_id == (bouquet_meta.type_b_id if bouquet_meta else None), Integer) +
        flower_score
    ).label("match_score")

    query = (
        db.session.query(
            Bouquet.bouquet_id,
            Bouquet.bouquet_name,
            Bouquet.bouquet_price,
            Bouquet.bouquet_image,
            Bouquet.size_id,
            Meta.occasion_id,
            Meta.whom_id,
            Meta.type_b_id,
            match_score
        )
        .filter(Bouquet.bouquet_id != bouquet_id)
        .outerjoin(Meta, Bouquet.bouquet_id == Meta.bouquet_id)
        .outerjoin(BouquetSet, Bouquet.bouquet_id == BouquetSet.bouquet_id)
        .group_by(
            Bouquet.bouquet_id,
            Bouquet.bouquet_name,
            Bouquet.bouquet_price,
            Bouquet.bouquet_image,
            Bouquet.size_id,
            Meta.occasion_id,
            Meta.whom_id,
            Meta.type_b_id
        )
        .having(match_score >= 2)
        .order_by(match_score.desc())
    )

    for key, value in filters.items():
        if value:
            if key == "occasion_id":
                query = query.filter(or_(Meta.occasion_id == None, Meta.occasion_id == value))
            elif key == "whom_id":
                query = query.filter(or_(Meta.whom_id == None, Meta.whom_id == value))
            elif key == "type_b_id":
                query = query.filter(or_(Meta.type_b_id == None, Meta.type_b_id == value))
            elif key == "size_id":
                query = query.filter(or_(Bouquet.size_id == None, Bouquet.size_id == value))
            elif key == "color_id":
                pass  # не використовується

    results = query.all()

    # 🔁 Фільтруємо унікальні букети
    seen_ids = set()
    unique_results = []
    for r in results:
        if r.bouquet_id not in seen_ids:
            seen_ids.add(r.bouquet_id)
            unique_results.append({
                "bouquet_id": r.bouquet_id,
                "bouquet_name": r.bouquet_name,
                "bouquet_price": r.bouquet_price,
                "bouquet_image": r.bouquet_image
            })

        if len(unique_results) >= 6:
            break

    return unique_results

