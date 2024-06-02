from flask import Flask
from app.common.config import Config
from app.common.extensions import db
from app.common.models import Item, Recommend
from app.item.Embedding.routes import embedding_bp
from app.item.Cookie.routes import cookie_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()

    logging.basicConfig(level=app.config.get("LOGGING_LEVEL", "DEBUG"))
    app.register_blueprint(embedding_bp, url_prefix='/api')
    app.register_blueprint(cookie_bp, url_prefix='/api')
    return app
