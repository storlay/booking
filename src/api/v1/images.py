from fastapi import APIRouter
from fastapi import UploadFile

from src.services.media import MediaService


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.post(
    "/upload",
)
def upload_image(
    file: UploadFile,
) -> None:
    return MediaService().upload_image(
        file=file,
    )
