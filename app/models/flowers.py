from app.extensions import db


class FlowerDetails(db.Model):
    __tablename__ = "flowers"

    id = db.Column(db.Integer, primary_key=True)
    flower_id = db.Column(db.Integer, db.ForeignKey("flower.flower_id"))
    flower_price = db.Column(db.Integer, nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey("size.size_id"))
    color_id = db.Column(db.Integer, db.ForeignKey("color.color_id"))
    flower_image = db.Column(db.String(255))