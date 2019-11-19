import logging
from unittest.mock import MagicMock
from jobs.util.test_base import IntegrationTestCase
from jobs.scheduler.cleanup_job import CleanupJob


class TestCleanupJob(IntegrationTestCase):
    def test_job(self):
        CleanupJob().perform()
