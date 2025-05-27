from app.extensions import db


class Customer(db.Model):
    __tablename__ = "customer"

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(30))
    customer_surname = db.Column(db.String(30))
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(100))
    customer_area = db.Column(db.Enum('Індустріальний','Київський','Немишлянський','Новобаварський',
                                      'Основʼянський','Салтівський','Слобідський','Холодногірський','Шевченковський'))
    customer_steet_and_number = db.Column(db.String(100))
    customer_entrance = db.Column(db.Integer)

    orders = db.relationship("Order", backref="customer", lazy=True)
