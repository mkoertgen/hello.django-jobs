import os
from flask import Blueprint, render_template

# from api.jobs import Jobs


pages = Blueprint('pages', __name__)

REPO_URL = 'https://github.com/mkoertgen/hello.django-jobs'


@pages.route('/')
def index():
    app = {
        'git': REPO_URL,
        'wiki': f'{REPO_URL}/wiki'
    }
    return render_template('index.html', app=app)


@pages.route('/about')
def about():
    git = {
        'commit': os.environ.get('OPENSHIFT_BUILD_COMMIT', 'master'),
        'repository': {
            'source': os.environ.get('OPENSHIFT_BUILD_SOURCE', REPO_URL),
            'commits': f"{REPO_URL}/commits"
        }
    }
    return render_template('about.html', git=git)


@pages.route('/jobs')
def jobs():
    # TODO
    return index()


@pages.route('/api')
def api():
    # TODO
    return index()
