from enum import Enum
from typing import Optional

from fastapi import Query, Body
from pydantic import BaseModel

from workflow import ImageRes, ComfySettings, Workflow


class ImageSize(str, Enum):
    Square = "square"
    Portrait = "portrait"
    Landscape = "landscape"


prompt_query = Query(
    ...,
    min_length=1,
    max_length=1000,
    description="The prompt to generate an image for.",
    example="A cozy cabin in the woods made of gingerbread",
)

width_query = Query(
    default=None,
    ge=16,
    le=1024,
    description=(
        "Overrides the default width determined by `size`. "
        "Leave empty to use the default."
    ),
    example=None,
)

height_query = Query(
    default=None,
    ge=16,
    le=1024,
    description=(
        "Overrides the default height determined by `size`. "
        "Leave empty to use the default."
    ),
    example=None,
)

seed_query = Query(
    default=None,
    description="Will be used as the seed for image generation (Default: random). Can be an integer or string.",
    example=None,
)

imagesize_query = Query(
    default=ImageSize.Landscape,
    description="Choose between 1:1, 2:3 or 3:2. 512px on the short side. Ignored if width and height are specified.",
)

imagerequest_body = Body(
    ...,
    examples=[
        {"prompt": "A cozy cabin in the woods", "width": 512, "height": 512},
    ],
)


class ImageRequest(BaseModel):
    prompt: str = prompt_query
    size: Optional[ImageSize] = imagesize_query
    width: Optional[int] = width_query
    height: Optional[int] = height_query
    seed: Optional[str | int] = seed_query


def get_image_res(size: ImageSize) -> ImageRes:
    match size:
        case ImageSize.Square:
            return ImageRes(512, 512)
        case ImageSize.Portrait:
            return ImageRes(512, 768)
        case _:
            return ImageRes(768, 512)


def construct_workflow(
    request: ImageRequest,
) -> Workflow:
    prompt = request.prompt
    size = request.size or ImageSize.Landscape
    width = request.width
    height = request.height
    seed = request.seed

    if request.width and request.height:
        settings = ComfySettings(res=ImageRes(width=width, height=height))
    else:
        settings = ComfySettings(res=get_image_res(size))

    if isinstance(seed, str):
        try:
            settings.seed = int(seed)
        except ValueError:
            settings.seed = abs(hash(seed)) % (10**8)

    return Workflow(prompt=prompt, settings=settings)
