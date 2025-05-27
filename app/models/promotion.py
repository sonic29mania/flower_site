from app.extensions import db


class Promotion(db.Model):
    __tablename__ = "promotion"

    promo_id = db.Column(db.Integer, primary_key=True)
    promo_name = db.Column(db.String(50), nullable=False)
    discount_percent = db.Column(db.Numeric(5,2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)