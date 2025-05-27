from flask import Blueprint, render_template

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route("/delivery")
def delivery():
    return render_template("delivery.html")
