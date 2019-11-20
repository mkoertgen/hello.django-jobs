import uuid
from django.db import models
from django.utils import timezone


class JobModel(models.Model):
    ENQUEUED = u"Enqueued"
    STARTED = u"Started"
    ERROR = u"Error"
    SUCCESS = u"Executed"
    STATES = [ENQUEUED, STARTED, ERROR, SUCCESS]

    BADGES = {ERROR: 'badge-danger', SUCCESS: 'badge-success'}
    BADGE_DEFAULT = 'badge-secondary'

    # We want indepence of the server when generating ids
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    job_class = models.CharField(max_length=200)
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default=ENQUEUED, choices=[[x, x] for x in STATES])
    logs = models.TextField()
    # What is the maximum length of a URL in different browsers? https://stackoverflow.com/a/417184
    result_link = models.CharField(max_length=2000, default='', blank=True, null=True)

    @property
    def name(self) -> str:
        return self.job_class

    @property
    def duration(self) -> float:
        if self.started is None:
            return None
        current = self.finished if self.finished else timezone.now()
        return (current - self.started).total_seconds()

    def badge_class(self) -> str:
        return JobModel.BADGES.get(self.status, JobModel.BADGE_DEFAULT)

    def is_running(self) -> bool:
        return not self.status in [JobModel.ERROR, JobModel.SUCCESS]

    def has_result(self) -> bool:
        return bool(self.result_link)

    def log(self, msg: str, save: bool = True):
        self.logs += msg
        if save:
            self.save()  # update_fields=['logs'])

    def start(self, *args):
        self.status = JobModel.STARTED
        self.started = timezone.now()

    def succeed(self):
        self.status = JobModel.SUCCESS
        self.finished = timezone.now()

    def fail(self, e: Exception):
        self.status = JobModel.ERROR
        self.finished = timezone.now()

    def get_absolute_url(self) -> str:
        from django.urls import reverse
        return reverse('job', kwargs={'pk': self.id})
