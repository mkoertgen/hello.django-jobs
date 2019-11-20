import datetime
import os
from django.db.models import Q
from jobs.scheduler.jobs import BaseJob
from jobs.models import JobModel


class CleanupJob(BaseJob):
    SCHEDULE = os.environ.get('CLEANUP_JOB_CRON', '0 0 * * 0')
    DAYS_AGO = int(os.environ.get('CLEANUP_JOB_DAYS', '3'))

    def _run(self, *args):
        days_ago = datetime.datetime.now() - datetime.timedelta(days=CleanupJob.DAYS_AGO)

        self.logger.info("Removing old job executions before '%s' OR 'enqueued'...", days_ago)
        old_jobs = JobModel.objects.filter(Q(updated_at__lt=days_ago) | Q(status=JobModel.ENQUEUED))
        if not old_jobs.exists():
            self.logger.info('No obsolete job exceutions.')
            return
        count = old_jobs.count()
        old_jobs._raw_delete(old_jobs.db)
        self.logger.info("Deleted '%s' old job executions.", count)
