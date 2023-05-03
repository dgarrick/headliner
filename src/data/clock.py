from main import dump_clusters
from apscheduler.schedulers.blocking import BlockingScheduler

dump_clusters()
sched = BlockingScheduler()
sched.start()

@sched.interval_schedule(hours=6)
def timed_clusters():
    dump_clusters()
