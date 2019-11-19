import datetime
import os
from .jobs import BaseJob
from .job_model import JobModel


class CleanupJob(BaseJob):
    SCHEDULE = os.environ.get('CLEANUP_JOB_CRON', '0 0 * * 0')
    DAYS_AGO = int(os.environ.get('CLEANUP_JOB_DAYS', '3'))

    def _run(self, *args):
        days_ago = datetime.datetime.now() - datetime.timedelta(days=CleanupJob.DAYS_AGO)
        old_jobs = JobModel.query.filter(updated_at__lt=days_ago)
        # old_jobs._raw_delete(old_jobs.db)
        old_jobs.delete()
        # TODO: commit?
