import os
from urllib.parse import urlparse
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from pages.controllers import pages
#from api.controllers import api

app = Flask(__name__)

# --- Add blueprints here
app.register_blueprint(pages, url_prefix='/')
#app.register_blueprint(api, url_prefix='/api')

# --- health checks
health = HealthCheck()
envdump = EnvironmentDump()


# Add a flask route to expose information
app.add_url_rule("/api/health", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/api/env", "environment",
                 view_func=lambda: envdump.run())

# --- common flask filters
@app.template_filter()
def hostname(request):
    return urlparse(request.base_url).hostname


# --- common flask context processors
@app.context_processor
def inject_env():
    return dict(env=os.environ)


# --- main entry point
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
