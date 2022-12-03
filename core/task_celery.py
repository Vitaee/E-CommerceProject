from .settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CELERY_TASKS_REGISTER
import time
from celery import Celery


celery = Celery(__name__, include=CELERY_TASKS_REGISTER)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


celery.autodiscover_tasks()


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True


@celery.task(name="create_test_task")
def create_test_task(task_type):
    time.sleep(int(task_type) * 5)
    return True

#create_test_task(2)