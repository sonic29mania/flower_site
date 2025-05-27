from app.extensions import db



class Size(db.Model):
    __tablename__ = "size"

    size_id = db.Column(db.Integer, primary_key=True)
    size_name = db.Column(db.String(30), nullable=False)
    size = db.Column(db.Enum('S', 'M', 'L', 'XL'))
