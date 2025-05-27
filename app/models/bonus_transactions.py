from app.extensions import db


class BonusTransaction(db.Model):
    __tablename__ = "bonus_transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    change_amount = db.Column(db.Integer)
    reason = db.Column(db.String(100))
    transaction_date = db.Column(db.DateTime)