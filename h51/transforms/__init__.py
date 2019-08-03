
__all__ = ['Analyzer']


class Transform:
    """
    Transforms are run against images in order to create a new variation of
    the image (such as resizing an image or storing it in a web safe format).
    """

    def __init__(self, name, **kwargs):

        # The name of the analyzer
        self._name = name

        # The arguments for the analyzer
        self._args = {k: v for k, v in kwargs.items() if v is not None}

    def to_json_type(self):
        return [self._name, self._args]


from . import images

