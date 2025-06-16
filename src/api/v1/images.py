import shutil

from fastapi import APIRouter
from fastapi import UploadFile

from src.tasks.tasks import resize_image


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.post(
    "/upload",
)
def upload_image(
    file: UploadFile,
):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)