from app.extensions import db


class OrderBouquet(db.Model):
    __tablename__ = "orders_bouquet"
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), primary_key=True)
    bouquet_id = db.Column(db.Integer, db.ForeignKey("bouquet.bouquet_id"), primary_key=True)
    ordered_quantity = db.Column(db.Integer)

    bouquet = db.relationship("Bouquet", backref="order_links")
