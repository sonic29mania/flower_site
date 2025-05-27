from app.extensions import db


class DeliveryTracking(db.Model):
    __tablename__ = "delivery_tracking"

    delivery_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))
    status = db.Column(db.Enum('Готується', 'Передано кур’єру', 'У дорозі', 'Доставлено'))
    status_time = db.Column(db.DateTime)
