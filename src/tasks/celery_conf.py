from celery import Celery
from celery.schedules import crontab

from src.config import settings


celery_app = Celery(
    "booking-tasks",
    broker=settings.redis.URL,
    include=[
        "src.tasks.tasks",
    ],
)
celery_app.conf.beat_schedule = {
    "booking_today_checkin": {
        "task": "booking_today_checkin",
        "schedule": crontab(hour="9"),
    }
}
