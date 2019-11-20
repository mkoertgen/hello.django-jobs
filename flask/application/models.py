import uuid
from datetime import datetime
from contextlib import contextmanager
from .db import db, session_scope


class JobModel(db.Model):
    ENQUEUED = u"Enqueued"
    STARTED = u"Started"
    ERROR = u"Error"
    SUCCESS = u"Executed"
    STATES = [ENQUEUED, STARTED, ERROR, SUCCESS]
    # bulma.io, cf.: https://bulma.io/documentation/elements/tag/#colors
    BADGES = {ERROR: 'is-danger', SUCCESS: 'is-success'}
    BADGE_DEFAULT = 'is-info'

    #id = db.Column(db.Integer, primary_key=True)
    # We want indepence of the server when generating ids
    id = db.Column(db.String(36), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)

    job_class = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum(*STATES), default=ENQUEUED)
    logs = db.Column(db.Text)
    # What is the maximum length of a URL in different browsers? https://stackoverflow.com/a/417184
    # blank=True, null=True)
    result_link = db.Column(db.String(2000))

    def __init__(self, **kwargs):
        super(JobModel, self).__init__(**kwargs)
        self.id = str(uuid.uuid4())
        self.logs = ''
        self.result_link = None
        self.status = JobModel.ENQUEUED
        self.session = None
        db.session.add(self)
        db.session.commit()

    @property
    def name(self) -> str:
        return self.job_class

    @property
    def duration(self) -> float:
        current = datetime.now() if self.is_running else self.updated_at
        return current - self.created_at

    @property
    def badge_class(self) -> str:
        return JobModel.BADGES.get(self.status, JobModel.BADGE_DEFAULT)

    @property
    def is_running(self) -> bool:
        return not self.status in [JobModel.ERROR, JobModel.SUCCESS]

    @property
    def has_result(self) -> bool:
        return bool(self.result_link)

    def log(self, msg: str, save: bool = True):
        if self.session is None:
            return
        self.logs += msg
        if save:
            self.save()

    @contextmanager
    def start(self, app, *args):
        with app.app_context() as ctx, session_scope() as session:
            self.session = session
            self.status = JobModel.STARTED
            self.save()
            yield self.session
            self.save()
            self.session = None

    def save(self):
        self.updated_at = datetime.now()
        self.session.merge(self)
        self.session.commit()

    def succeed(self):
        self.status = JobModel.SUCCESS

    def fail(self, _: Exception):
        self.status = JobModel.ERROR
