import src.data.main
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
sched.start()

@sched.interval_schedule(hours=6)
def timed_clusters():
    main.dump_clusters()

