from app.extensions import db
from app.models.flower import Flower
from app.models.color import Color

class BouquetSet(db.Model):
    __tablename__ = "bouquet_set"
    bouquet_id = db.Column(db.Integer, db.ForeignKey("bouquet.bouquet_id"), primary_key=True)
    flower_id = db.Column(db.Integer, db.ForeignKey("flower.flower_id"), primary_key=True)
    flower_color_id = db.Column(db.Integer, db.ForeignKey("color.color_id"))
    quantity = db.Column(db.Integer, nullable=False)
    flower = db.relationship("Flower", backref="bouquet_sets")
    color = db.relationship("Color", backref="bouquet_sets")