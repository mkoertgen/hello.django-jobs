from flask_humanize import Humanize
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
humanize = Humanize()


def create_app(start_jobs: bool = False):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('settings')

    db.init_app(app)
    migrate.init_app(app, db)
    humanize.init_app(app)

    with app.app_context():
        # -- Add humanize middleware

        # -- Add blueprints here
        from .jobs.controllers import jobs
        from .pages.controllers import pages
        #from api.controllers import api
        app.register_blueprint(pages, url_prefix='/')
        app.register_blueprint(jobs, url_prefix='/jobs')
        #app.register_blueprint(api, url_prefix='/api')

        # -- health checks
        from healthcheck import HealthCheck, EnvironmentDump
        health = HealthCheck()
        envdump = EnvironmentDump()
        # Add a flask route to expose information
        app.add_url_rule("/api/health", "healthcheck",
                         view_func=health.run)
        app.add_url_rule("/api/env", "environment",
                         view_func=envdump.run)

        if start_jobs:
            from application.jobs.jobs import Jobs
            Jobs.start()
        return app
