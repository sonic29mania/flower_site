from flask import Blueprint, render_template, request, url_for
from app.models.bouquet import Bouquet
from app.models.bouquet_1 import BouquetMeta
from app.models.color import Color
from app.models.size import Size
from app.models.type_b import TypeB
from app.models.occasion import Occasion
from app.models.whom import Whom
from sqlalchemy import or_
import math

category_bp = Blueprint('category', __name__)

@category_bp.route('/category')
def category():
    type_ids = request.args.getlist("type", type=int)
    occ_ids = request.args.getlist("occasion", type=int)
    whom_ids = request.args.getlist("whom", type=int)
    color_ids = request.args.getlist("color", type=int)
    size_ids = request.args.getlist("size", type=int)
    price_sort = request.args.get("price", default="")
    page = request.args.get("page", default=1, type=int)

    per_page = 12

    query = Bouquet.query.filter_by(bouquet_obviousness="Наявний")
    query = query.outerjoin(BouquetMeta, Bouquet.bouquet_id == BouquetMeta.bouquet_id)

    if type_ids:
        query = query.filter(or_(BouquetMeta.type_b_id == None, BouquetMeta.type_b_id.in_(type_ids)))
    if occ_ids:
        query = query.filter(or_(BouquetMeta.occasion_id == None, BouquetMeta.occasion_id.in_(occ_ids)))
    if whom_ids:
        query = query.filter(or_(BouquetMeta.whom_id == None, BouquetMeta.whom_id.in_(whom_ids)))
    if color_ids:
        query = query.filter(or_(Bouquet.color_id == None, Bouquet.color_id.in_(color_ids)))
    if size_ids:
        query = query.filter(or_(Bouquet.size_id == None, Bouquet.size_id.in_(size_ids)))

    if price_sort == "asc":
        query = query.order_by(Bouquet.bouquet_price.asc())
    elif price_sort == "desc":
        query = query.order_by(Bouquet.bouquet_price.desc())

    query = query.distinct(Bouquet.bouquet_id)
    total = query.count()
    bouquets = query.paginate(page=page, per_page=per_page, error_out=False).items
    total_pages = math.ceil(total / per_page)

    for bouquet in bouquets:
        bouquet.image_url = "/static" + bouquet.bouquet_image if bouquet.bouquet_image else ""

    types = TypeB.query.all()
    occasions = Occasion.query.all()
    whoms = Whom.query.all()
    colors = Color.query.all()
    sizes = Size.query.all()

    def build_url(page_num):
        query_args = request.args.to_dict(flat=False)
        query_args['page'] = [str(page_num)]
        return url_for('category.category') + '?' + '&'.join(
            f"{key}={value}" if isinstance(value, str) else '&'.join([f"{key}={v}" for v in value])
            for key, value in query_args.items()
        )

    page_links = {
        "prev": build_url(page - 1) if page > 1 else None,
        "next": build_url(page + 1) if page < total_pages else None
    }

    return render_template("category.html",
                           bouquets=bouquets,
                           types=types,
                           occasions=occasions,
                           whoms=whoms,
                           colors=colors,
                           sizes=sizes,
                           selected_type=type_ids,
                           selected_occ=occ_ids,
                           selected_whom=whom_ids,
                           selected_color=color_ids,
                           selected_size=size_ids,
                           selected_price_sort=price_sort,
                           current_page=page,
                           total_pages=total_pages,
                           page_links=page_links)

@category_bp.route("/category/load_more")
def load_more():
    type_ids = request.args.getlist("type", type=int)
    occ_ids = request.args.getlist("occasion", type=int)
    whom_ids = request.args.getlist("whom", type=int)
    color_ids = request.args.getlist("color", type=int)
    size_ids = request.args.getlist("size", type=int)
    price_sort = request.args.get("price", default="")
    page = request.args.get("page", default=1, type=int)

    per_page = 12

    query = Bouquet.query.filter_by(bouquet_obviousness="Наявний")
    query = query.outerjoin(BouquetMeta, Bouquet.bouquet_id == BouquetMeta.bouquet_id)

    if type_ids:
        query = query.filter(or_(BouquetMeta.type_b_id == None, BouquetMeta.type_b_id.in_(type_ids)))
    if occ_ids:
        query = query.filter(or_(BouquetMeta.occasion_id == None, BouquetMeta.occasion_id.in_(occ_ids)))
    if whom_ids:
        query = query.filter(or_(BouquetMeta.whom_id == None, BouquetMeta.whom_id.in_(whom_ids)))
    if color_ids:
        query = query.filter(or_(Bouquet.color_id == None, Bouquet.color_id.in_(color_ids)))
    if size_ids:
        query = query.filter(or_(Bouquet.size_id == None, Bouquet.size_id.in_(size_ids)))

    if price_sort == "asc":
        query = query.order_by(Bouquet.bouquet_price.asc())
    elif price_sort == "desc":
        query = query.order_by(Bouquet.bouquet_price.desc())

    query = query.distinct(Bouquet.bouquet_id)
    bouquets = query.paginate(page=page, per_page=per_page, error_out=False).items

    for bouquet in bouquets:
        bouquet.image_url = "/static" + bouquet.bouquet_image if bouquet.bouquet_image else ""

    return render_template("_bouquets.html", bouquets=bouquets)