import src.data.main
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
sched.start()

@sched.interval_schedule(minutes=1)
def timed_clusters():
    main.dump_clusters()

