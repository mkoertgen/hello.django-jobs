import random
import time
from jobs.scheduler.jobs import BaseJob


class SampleJob(BaseJob):
  def _run(self, *args):
    time.sleep(random.randrange(1, 100, 1)/100.)
