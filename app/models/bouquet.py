from app.extensions import db
from app.models.size import Size
from app.models.color import Color
from app.models.bouquet_1 import BouquetMeta
from app.models.bouquet_set import BouquetSet

class Bouquet(db.Model):
    __tablename__ = "bouquet"
    bouquet_id = db.Column(db.Integer, primary_key=True)
    bouquet_name = db.Column(db.String(30), nullable=False)
    bouquet_price = db.Column(db.Integer, nullable=False)
    bouquet_seasonal_price = db.Column(db.Integer, nullable=False)
    bouquet_obviousness = db.Column(db.Enum('Наявний', 'Ненаявний'))
    size_id = db.Column(db.Integer, db.ForeignKey("size.size_id"))
    bouquet_image = db.Column(db.String(255))
    size = db.relationship("Size", backref="bouquets")
    meta = db.relationship("BouquetMeta", backref="bouquet", uselist=False)
    sets = db.relationship("BouquetSet", backref="bouquet")