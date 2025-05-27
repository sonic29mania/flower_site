from app.extensions import db


class TypeB(db.Model):
    __tablename__ = "type_b"

    type_b_id = db.Column(db.Integer, primary_key=True)
    type_b_name = db.Column(db.String(30), nullable=False)
