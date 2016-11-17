import src.data.main
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=6)
def timed_clusters():
    main.dump_clusters()

sched.start()
