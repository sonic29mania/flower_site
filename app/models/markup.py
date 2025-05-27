from app.extensions import db


class Markup(db.Model):
    __tablename__ = "markup"

    markup_id = db.Column(db.Integer, primary_key=True)
    target_type = db.Column(db.Enum('flower', 'bouquet'))
    target_id = db.Column(db.Integer)
    percent = db.Column(db.Numeric(5,2))
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)
