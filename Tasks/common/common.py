import app
from Tasks.Scheduler import Scheduler

Scheduler = Scheduler(app)

@Scheduler.scheduler.task('interval', id='my_task', seconds=5)
def my_background_task():
    print("Running background task...")