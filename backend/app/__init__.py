from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from ..config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    from .api.department import department as department_blueprint
    app.register_blueprint(department_blueprint, url_prefix='/api/department')
    from .api.project import project as project_blueprint
    app.register_blueprint(project_blueprint, url_prefix='/api/project')

    return app
