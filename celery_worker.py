from app.workers.tasks import celery

celery.autodiscover_tasks(["app.workers"])