from app.extensions import db


class Ribbon(db.Model):
    __tablename__ = "ribbon"

    ribbon_id = db.Column(db.Integer, primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey("color.color_id"))
    price_per_roll = db.Column(db.Numeric(6, 2))
    length_meters = db.Column(db.Integer, default=25)
    price_per_bouquet = db.Column(db.Numeric(6, 2))
    image = db.Column(db.String(255))
