import asyncio
import os

from PIL import Image

from src.config import settings
from src.tasks.celery_conf import celery_app
from src.tasks.utils import get_bookings_for_notify_checkin


@celery_app.task
def resize_image(
    image_path: str,
    sizes: list[int] = settings.models.DEFAULT_IMAGE_SIZES,
) -> None:
    image = Image.open(image_path)
    name, ext = os.path.splitext(os.path.basename(image_path))
    for size in sizes:
        resized_image = image.resize(
            (size, int(image.height * (size / image.width))),
            Image.Resampling.LANCZOS,
        )
        new_file_name = f"{name}_{size}px{ext}"
        file_path = os.path.join(
            settings.models.DEFAULT_IMAGE_PATH,
            new_file_name,
        )
        resized_image.save(file_path)


@celery_app.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin() -> None:
    asyncio.run(get_bookings_for_notify_checkin())