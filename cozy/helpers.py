from schema import ImageRequest, ImageSize
from workflow import ImageRes, ComfySettings, Workflow


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

    settings.steps = request.steps

    return Workflow(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        settings=settings,
    )
