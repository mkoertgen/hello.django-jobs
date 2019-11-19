import glob
import importlib
import logging
from os.path import basename, dirname, isfile, join

import inflection
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from application.models import JobModel


class LogCapture(object):
    # cf.: https://stackoverflow.com/a/9534960
    def __init__(self, stream, logger=None):
        self.logger = logger if logger else logging.getLogger()
        self.handler = logging.StreamHandler(stream)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%dT%H:%M:%S%z')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def __del__(self):
        self.__close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __close(self):
        self.logger.removeHandler(self.handler)
        self.handler.close()


class BaseJob(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.job_model = JobModel(job_class=self.name)

    def _run(self, *args):
        raise NotImplementedError

    def perform(self, *args):
        with LogCapture(self):
            try:
                self.logger.info("Started with args='%s'", args)
                self.job_model.start(args)
                self._run(args)
                self.job_model.succeed()
                self.logger.info('Succeeded.')
            except Exception as e:
                self.logger.warning("Failed: %s", e)
                self.job_model.fail(e)
            finally:
                self.logger.info('Stopped (duration: %s)',
                                 self.job_model.duration)

    def perform_later(self, *args):
        return self._enqueue(None, args)

    def schedule(self, cron_tab: str):
        cron = CronTrigger.from_crontab(cron_tab)
        return self._enqueue(cron)

    def _enqueue(self, trigger: BaseTrigger, *args) -> Job:
        return Jobs.scheduler.add_job(self.perform, trigger=trigger,
                                      name=self.__class__.__name__,
                                      args=args, replace_existing=True)

    # stream implementation for logging, cf.:
    # - https://pysnippet.blogspot.com/2009/10/file-like-objects.html
    def write(self, msg: str):
        self.job_model.log(msg)

    def close(self):
        pass


class Jobs():
    logger = logging.getLogger(__name__)
    scheduler = BackgroundScheduler()
    started = False
    ALL_JOBS = {}

    @staticmethod
    def all():
        return Jobs.ALL_JOBS

    @staticmethod
    def get(name: str):
        return Jobs.all()[name]

    @staticmethod
    def start():
        if Jobs.started:
            raise ValueError('Already started')
        Jobs.scheduler.add_jobstore(MemoryJobStore())
        Jobs._discover_jobs()
        Jobs._schedule_jobs()
        Jobs.scheduler.start()
        Jobs.started = True

    @staticmethod
    def create(name: str) -> BaseJob:
        return Jobs.get(name)['class']()

    @staticmethod
    def schedule(name: str, cron_tab: str = None):
        if cron_tab is None:
            cron_tab = Jobs.get(name)['schedule']
        if not cron_tab is None:
            job = Jobs.create(name)
            job.schedule(cron_tab)
            Jobs.logger.debug(
                "Scheduled job '%s' (schedule '%s')", name, cron_tab)

    @staticmethod
    def _discover_jobs():
        modules = glob.glob(join(dirname(__file__), '[!test_]*_job.py'))
        job_modules = [basename(f)[:-3] for f in modules if isfile(f)]
        Jobs.logger.debug('Discovering jobs...')
        for job_module in job_modules:
            job_class_name = inflection.camelize(job_module)
            module = importlib.import_module(f'application.jobs.{job_module}')
            job_class = getattr(module, job_class_name)
            schedule = getattr(job_class, 'SCHEDULE', None)
            name = job_class.__name__
            Jobs.logger.debug(
                "Discovered job '%s' (schedule '%s')", name, schedule)
            Jobs.ALL_JOBS[name] = {
                'class': job_class,
                'schedule': schedule
            }

    @staticmethod
    def _schedule_jobs():
        Jobs.logger.debug('Scheduling jobs...')
        for name in Jobs.all().keys():
            Jobs.schedule(name)
