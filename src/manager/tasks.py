from celery import shared_task
from time import sleep, time
from manager.models import TableAggregate


@shared_task
def hello(pause):
	sleep(pause)
	return "hello, task done"


@shared_task
def create_aggregate(user_id):
	sleep(10)
	TableAggregate.objects.create(user_id=user_id, result=int(time()))

@shared_task
def just_taks():
	return "hello done"


