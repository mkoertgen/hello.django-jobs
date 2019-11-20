import datetime
import os
from application.models import JobModel
from .jobs import BaseJob


class CleanupJob(BaseJob):
    SCHEDULE = os.environ.get('CLEANUP_JOB_CRON', '0 0 * * 0')
    DAYS_AGO = int(os.environ.get('CLEANUP_JOB_DAYS', '3'))

    def _run(self, *_):
        self.job_model.result_link = '/jobs'  # url_for('jobs.index')

        days_ago = datetime.datetime.now() - datetime.timedelta(days=CleanupJob.DAYS_AGO)
        self.logger.info("Removing old job before '%s'...", days_ago)
        old_jobs = self.session.query(JobModel).filter(
            JobModel.updated_at <= days_ago)
        count = old_jobs.count()
        if count < 1:
            self.logger.info('No obsolete jobs')
            return

        old_jobs.delete()
        self.session.commit()
        self.logger.info("Deleted '%s' old jobs", count)
