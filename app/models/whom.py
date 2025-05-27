from app.extensions import db


class Whom(db.Model):
    __tablename__ = "whom"

    whom_id = db.Column(db.Integer, primary_key=True)
    whom_name = db.Column(db.String(30), nullable=False)