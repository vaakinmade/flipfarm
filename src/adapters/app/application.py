from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.main.containers import Container

from src.adapters.app.blueprints import investment_blueprint, user_blueprint, home_blueprint, commodity_blueprint
from src.main import config


db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    container = Container()
    app = Flask(__name__)

    # loads all the env variable constants from config
    app.config.from_object(config)
    app.container = container

    # initialise app with SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://simba:{config.PG_PASSWORD}@35.246.25.244/simba_db"

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(investment_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(commodity_blueprint)
    app.add_url_rule("/", endpoint="index")
    return app
