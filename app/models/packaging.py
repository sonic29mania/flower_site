from app.extensions import db


class Packaging(db.Model):
    __tablename__ = "packaging"

    packaging_id = db.Column(db.Integer, primary_key=True)
    packaging_name = db.Column(db.String(100), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey("color.color_id"))
    unit_price = db.Column(db.Numeric(6, 2), nullable=False)
    sheets_per_pack = db.Column(db.Integer, default=20)
    total_stock_packs = db.Column(db.Integer, default=10)
    image = db.Column(db.String(255))