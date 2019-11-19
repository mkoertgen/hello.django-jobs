import os
from urllib.parse import urlparse
from application import create_app

app = create_app(__name__ == '__main__')

# -- common flask filters
@app.template_filter()
def hostname(request):
    return urlparse(request.base_url).hostname


# -- common flask context processors
@app.context_processor
def inject_env():
    return dict(env=os.environ)


# --- main entry point
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
