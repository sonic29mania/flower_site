DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flowerTaleDiplom',
    'port': 3306
}

# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/FlowerTaleDiplom"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "xP@8gS!9eCz21kP3Tf$hKlv0!aBm"
