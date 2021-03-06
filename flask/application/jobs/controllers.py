import logging
import os
from flask import Blueprint, redirect, render_template, request, url_for

from application.db import db
from .jobs import Jobs
from application.models import JobModel

jobs = Blueprint('jobs', __name__)
LOGGER = logging.getLogger(__name__)


@jobs.route('/', methods=['GET'])
def index():
    # TODO: query params
    page = 0
    page_size = 10
    executions = JobModel.query.\
        order_by(JobModel.updated_at.desc()).\
        paginate(page, page_size, False).\
        items

    context = {
        'jobs': Jobs.all(),
        'executions': executions
    }
    return render_template('jobs.html', **context)


@jobs.route('/<id>', methods=['GET'])
def detail(id: str):
    job = JobModel.query.filter_by(id=id).first_or_404()
    return render_template('jobmodel_detail.html', job=job)


@jobs.route('/<job_class>/run', methods=['POST'])
def run(job_class: str):
    LOGGER.info("Scheduling '%s'...", job_class)
    job = Jobs.create(job_class)
    job.perform_later()
    return redirect(url_for('jobs.detail', id=job.job_model.id))


@jobs.route('/<id>/delete', methods=['POST', 'DELETE'])
def delete(id: str):
    job_model = JobModel.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('jobs.index'))
