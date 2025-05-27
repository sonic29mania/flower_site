from app.extensions import db


class PromoItem(db.Model):
    __tablename__ = "promo_items"

    id = db.Column(db.Integer, primary_key=True)
    promo_id = db.Column(db.Integer, db.ForeignKey("promotion.promo_id"))
    target_type = db.Column(db.Enum('flower', 'bouquet'))
    target_id = db.Column(db.Integer)
