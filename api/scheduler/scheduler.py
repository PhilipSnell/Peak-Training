from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def syncmfp():
    ...
    print("syncing mfp accounts")
    ...


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(syncmfp, 'interval', minutes=1, name='clean_accounts', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")