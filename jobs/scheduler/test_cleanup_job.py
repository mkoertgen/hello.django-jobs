import logging
from unittest.mock import MagicMock
from jobs.app.test_base import IntegrationTestCase
from jobs.scheduler.config_job import CleanupJob


class TestCleanupJob(IntegrationTestCase):
  def test_job(self):
    CleanupJob().perform()
