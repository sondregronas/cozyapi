from enum import Enum

from workflow import ImageRes


class ImageSize(str, Enum):
    Square = "square"
    Portrait = "portrait"
    Landscape = "landscape"


def get_image_res(size: ImageSize) -> ImageRes:
    match size:
        case ImageSize.Square:
            return ImageRes(512, 512)
        case ImageSize.Portrait:
            return ImageRes(512, 768)
        case _:
            return ImageRes(768, 512)
