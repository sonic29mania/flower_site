from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    order_date = db.Column(db.DateTime)
    subtotal = db.Column(db.Numeric(10, 2))
    delivery_type = db.Column(db.Enum('Самовивіз', 'Курєр'))
    delivery_fee = db.Column(db.Numeric(10, 2))
    discount_amount = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))
    delivery_address = db.Column(db.String(255))
    delivery_zone = db.Column(db.Enum('Індустріальний','Київський','Немишлянський','Новобаварський',
                                      'Основʼянський','Салтівський','Слобідський','Холодногірський','Шевченковський'))
    delivery_building = db.Column(db.String(50))
    delivery_entrance = db.Column(db.String(50))
    delivery_date = db.Column(db.Date)
    delivery_time = db.Column(db.Time)
    comment = db.Column(db.Text)
    order_status = db.Column(db.Enum('Очікує підтвердження','Обробляється','Доставляється','Завершено','Скасовано','Повернено'), default='Очікує підтвердження')

    bouquets = db.relationship("OrderBouquet", backref="order", lazy=True)
    delivery_tracking = db.relationship("DeliveryTracking", backref="order", lazy=True)