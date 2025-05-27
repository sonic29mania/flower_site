from app.extensions import db
from app.models.type_of_flowe import TypeOfFlower

class Flower(db.Model):
    __tablename__ = "flower"
    flower_id = db.Column(db.Integer, primary_key=True)
    flower_name = db.Column(db.String(50), nullable=False)
    type_f_id = db.Column(db.Integer, db.ForeignKey("type_of_flower.type_f_id"))
    flower_quantity = db.Column(db.Integer, nullable=False)
    type_f = db.relationship("TypeOfFlower", backref="flowers")