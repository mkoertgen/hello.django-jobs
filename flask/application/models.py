from datetime import datetime
from application import db


class JobModel(db.Model):
    ENQUEUED = u"Enqueued"
    STARTED = u"Started"
    ERROR = u"Error"
    SUCCESS = u"Executed"
    STATES = [ENQUEUED, STARTED, ERROR, SUCCESS]

    BADGES = {ERROR: 'badge-danger', SUCCESS: 'badge-success'}
    BADGE_DEFAULT = 'badge-secondary'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)

    job_class = db.Column(db.String(200), nullable=False)
    started = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    status = db.Column(db.Enum(*STATES), default=ENQUEUED)
    logs = db.Column(db.Text)
    # What is the maximum length of a URL in different browsers? https://stackoverflow.com/a/417184
    # blank=True, null=True)
    result_link = db.Column(db.String(2000))

    @property
    def name(self) -> str:
        return self.job_class

    @property
    def duration(self):
        if self.started is None:
            return None
        current = self.finished if self.finished else datetime.now()
        return current - self.started

    def badge_class(self) -> str:
        return JobModel.BADGES.get(self.status, JobModel.BADGE_DEFAULT)

    def is_running(self) -> bool:
        return not self.status in [JobModel.ERROR, JobModel.SUCCESS]

    def has_result(self) -> bool:
        return bool(self.result_link)

    def log(self, msg: str):
        self.logs = self.logs + msg if self.logs else msg

    def start(self, *args):
        self.status = JobModel.STARTED
        self.started = datetime.now()

    def succeed(self):
        self.status = JobModel.SUCCESS
        self.finished = datetime.now()

    def fail(self, _: Exception):
        self.status = JobModel.ERROR
        self.finished = datetime.now()
