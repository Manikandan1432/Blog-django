from background_task import background
import time

@background(schedule=10)
def my_timer():
    time.sleep(10)
    return 'task completed'