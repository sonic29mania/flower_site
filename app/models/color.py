from app.extensions import db


class Color(db.Model):
    __tablename__ = "color"

    color_id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(30), nullable=False)