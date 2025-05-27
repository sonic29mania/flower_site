from app.extensions import db


class Occasion(db.Model):
    __tablename__ = "occasion"

    occasion_id = db.Column(db.Integer, primary_key=True)
    occasion_name = db.Column(db.String(30), nullable=False)

