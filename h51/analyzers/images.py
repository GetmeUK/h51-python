
from . import Analyzer

__all__ = [
    'Animation',
    'DominantColors',
    'FocalPoint'
]


class Animation(Analyzer):
    """
    Extract animation information for an animated image.
    """

    def __init__(self):
        super().__init__('animation')


class DominantColors(Analyzer):
    """
    Extract a set of dominant colors from the image.
    """

    def __init__(self, max_colors=None, min_weight=None, max_sample_size=None):
        super().__init__(
            'dominant_colors',
            max_colors=max_colors,
            min_weight=min_weight,
            max_sample_size=max_sample_size
        )


class FocalPoint(Analyzer):
    """
    Detect the focal point within the image, by default the analyzer will
    automatically detect the focal point, however, the caller can also supply
    a focal point.
    """

    def __init__(self, top=None, left=None, bottom=None, right=None):

        super().__init__(
            'focal_point',
            top=top,
            left=left,
            bottom=bottom,
            right=right
        )
