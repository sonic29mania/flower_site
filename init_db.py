
from app import create_app
from app.extensions import db
from app.routes.cart import cart_bp

app = create_app()

with app.app_context():
    db.create_all()
    print("База даних ініціалізована.")
app.register_blueprint(cart_bp)