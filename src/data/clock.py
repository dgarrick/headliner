from main import dump_clusters
from apscheduler.schedulers.blocking import BlockingScheduler
import functions_framework


dump_clusters()
sched = BlockingScheduler()
sched.start()

@sched.interval_schedule(hours=6)
def timed_clusters():
    dump_clusters()
