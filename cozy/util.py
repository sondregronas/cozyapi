from enum import Enum

from workflow import ImageSize


class ImageSize(str, Enum):
    Square = "square"
    Portrait = "portrait"
    Landscape = "landscape"


def get_image_size(size: ImageSize) -> ImageSize:
    match size:
        case ImageSize.Square:
            return ImageSize(512, 512)
        case ImageSize.Portrait:
            return ImageSize(512, 768)
        case _:
            return ImageSize(768, 512)
