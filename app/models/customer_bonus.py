from app.extensions import db


class CustomerBonus(db.Model):
    __tablename__ = "customer_bonus"

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), primary_key=True)
    bonus_points = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime)