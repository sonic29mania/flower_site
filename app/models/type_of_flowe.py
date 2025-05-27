from app.extensions import db


class TypeOfFlower(db.Model):
    __tablename__ = "type_of_flower"

    type_f_id = db.Column(db.Integer, primary_key=True)
    type_f_name = db.Column(db.String(50), nullable=False)
    season = db.Column(db.Enum('Весна', 'Літо', 'Осінь', 'Зима', 'Круглорічно'), nullable=False)