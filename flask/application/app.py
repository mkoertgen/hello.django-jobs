import os
from urllib.parse import urlparse
from flask_humanize import Humanize
from flask import Flask
from .db import db, migrate

humanize = Humanize()


def create_app():
    app = Flask(__name__)
    app.config.from_object('application.settings')
    initialize_extensions(app)
    register_blueprints(app)
    register_filters(app)
    return app


def initialize_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    humanize.init_app(app)


def register_blueprints(app: Flask):
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


def register_filters(app: Flask):
    app.add_template_filter(hostname)
    app.template_context_processors[None].append(inject_env)


# -- common flask filters
def hostname(request):
    return urlparse(request.base_url).hostname


# -- common flask context processors
def inject_env():
    return dict(env=os.environ)
