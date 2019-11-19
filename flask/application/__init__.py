from flask_humanize import Humanize
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
humanize = Humanize()


def create_app():
    app = Flask(__name__)
    app.config.from_object('application.settings')
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    humanize.init_app(app)


def register_blueprints(app):
    # -- Add blueprints here
    from .jobs.controllers import jobs
    from .pages.controllers import pages
    # from api.controllers import api
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(jobs, url_prefix='/jobs')
    # app.register_blueprint(api, url_prefix='/api')

    # -- health checks
    from healthcheck import HealthCheck, EnvironmentDump
    health = HealthCheck()
    envdump = EnvironmentDump()
    # Add a flask route to expose information
    app.add_url_rule("/api/health", "healthcheck",
                     view_func=health.run)
    app.add_url_rule("/api/env", "environment",
                     view_func=envdump.run)
