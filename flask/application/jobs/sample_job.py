import random
import time
from .jobs import BaseJob


class SampleJob(BaseJob):
    def _run(self, *args):
        sleep_time = random.randrange(1, 100, 1)/10.
        self.logger.info("Sleeping '%s' seconds", sleep_time)
        time.sleep(sleep_time)
