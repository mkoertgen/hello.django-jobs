import os
import logging
from django.apps import AppConfig
from django.contrib.auth import get_user_model

LOGGER = logging.getLogger(__name__)


class JobsConfig(AppConfig):
    name = 'jobs'
    verbose_name = 'Scheduled Jobs for Django'

    def ready(self):
        try:
            JobsConfig.ensure_admin_user()
            from jobs.scheduler.jobs import Jobs
            Jobs.start()
        # pylint: disable=broad-except
        except Exception as ex:
            LOGGER.warning("%s (%s). Try running 'python manage.py migrate'",
                           ex, ex.__class__.__name__)
            return

    @staticmethod
    def ensure_admin_user():
        model = get_user_model()
        name = os.environ.get('ADMIN_USER', 'admin')
        if model.objects.filter(username=name).exists():
            LOGGER.info("Checked superuser '%s' exists", name)
        else:
            email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            password = os.environ.get('ADMIN_PWD', '123admin')
            model.objects.create_superuser(name, email, password)
            LOGGER.info("Created superuser '%s' (%s)", name, email)
