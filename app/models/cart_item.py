from app.extensions import db
from sqlalchemy.dialects.mysql import JSON

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False)
    bouquet_id = db.Column(db.Integer, db.ForeignKey('bouquet.bouquet_id'), nullable=True)
    is_custom = db.Column(db.Boolean, default=False)
    custom_flowers = db.Column(db.JSON, nullable=True)
    quantity = db.Column(db.Integer, default=1)
    custom_price = db.Column(db.Numeric(10, 2), nullable=True)  # ✅ обов’язково для правильного підрахунку


    def __repr__(self):
        return f"<CartItem {self.id}>"
