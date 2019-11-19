import logging
import os
from flask import Blueprint, render_template, request

from .jobs import Jobs
from .job_model import JobModel

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
    LOGGER.info("Executions %s", executions)

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
    return detail(job.job_model.id)


@jobs.route('/<id>/delete', methods=['POST', 'DELETE'])
def delete(id: str):
    JobModel.query.filter_by(id=id).delete()
    # TODO: commit
    return index()
