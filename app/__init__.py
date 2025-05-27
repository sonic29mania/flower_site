from flask import Flask
from flask_migrate import Migrate
from config import Config

from app.extensions import db  # <-- правильний db
# Імпортуєш всі Blueprints
from app.routes.main import main_bp
from app.routes.profile import profile_bp
from app.routes.category import category_bp
from app.routes.product import product_bp
from app.routes.constructor import constructor_bp
from app.routes.delivery import delivery_bp
from app.routes.sales import sales_bp
from app.routes.contacts import contacts_bp
from app.routes.login import login_bp
from app.routes.cart import cart_bp
from app.routes.auth import auth_bp

from app.routes.checkout import checkout_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)        
    Migrate(app, db)

    # Blueprint-и
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(constructor_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)
   
    app.register_blueprint(checkout_bp)

    return app
