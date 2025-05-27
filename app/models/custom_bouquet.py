from app.extensions import db


class CustomBouquet(db.Model):
    __tablename__ = "custom_bouquet"

    custom_bouquet_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    custom_name = db.Column(db.String(50))
    total_price = db.Column(db.Numeric(10,2))
    created_at = db.Column(db.DateTime)
