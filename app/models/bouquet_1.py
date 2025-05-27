from app.extensions import db
from app.models.type_b import TypeB
from app.models.occasion import Occasion
from app.models.whom import Whom

class BouquetMeta(db.Model):
    __tablename__ = "bouquet_1"
    bouquet_id = db.Column(db.Integer, db.ForeignKey("bouquet.bouquet_id"), primary_key=True)
    type_b_id = db.Column(db.Integer, db.ForeignKey("type_b.type_b_id"))
    occasion_id = db.Column(db.Integer, db.ForeignKey("occasion.occasion_id"))
    whom_id = db.Column(db.Integer, db.ForeignKey("whom.whom_id"))
    type_b = db.relationship("TypeB", backref="bouquet_metas")
    occasion = db.relationship("Occasion", backref="bouquet_metas")
    whom = db.relationship("Whom", backref="bouquet_metas")