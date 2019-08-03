
from . import Transform

__all__ = [
    'AutoOrient',
    'Crop',
    'Fit',
    'FocalPointCrop',
    'Output',
    'Rotate',
    'SingleFrame'
]


class AutoOrient(Transform):
    """
    Auto orient an image based on its Exif (Exchangeable image file format)
    data.
    """

    def __init__(self):
        super().__init__('auto_orient')


class Crop(Transform):
    """
    Crop an image.
    """

    def __init__(self, top, left, bottom, right):
        super().__init__(
            'crop',
            top=top,
            left=left,
            bottom=bottom,
            right=right
        )


class Fit(Transform):
    """
    Fit an image to a width/height.
    """

    def __init__(self, width, height, resample=None):
        super().__init__(
            'fit',
            width=width,
            height=height,
            resample=resample
        )


class FocalPointCrop(Transform):
    """
    Crop an image using around it's focal point (if no focal point is defined
    for the image the entire image will be considered the focal point).
    """

    def __init__(
        self,
        aspect_ratio=None,
        padding_top=None,
        padding_left=None,
        padding_bottom=None,
        padding_right=None
    ):
        super().__init__(
            'focal_point_crop',
            aspect_ratio=aspect_ratio,
            padding_top=padding_top,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            padding_right=padding_right
        )


class Output(Transform):
    """
    Output an image variation.
    """

    def __init__(
        self,
        image_format,
        quality=None,
        lossless=None,
        progressive=None,
        versioned=None
    ):
        super().__init__(
            'output',
            image_format=image_format,
            quality=quality,
            lossless=lossless,
            progressive=progressive,
            versioned=versioned
        )


class Rotate(Transform):
    """
    Rotate an image.
    """

    def __init__(self, degrees):
        super().__init__(
            'rotate',
            degrees=degrees
        )


class SingleFrame(Transform):
    """
    Extract a single frame from an animated image.
    """

    def __init__(self, frame_number=None):
        super().__init__(
            'single_frame',
            frame_number=frame_number
        )
