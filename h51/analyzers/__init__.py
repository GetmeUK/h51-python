
__all__ = ['Analyzer']


class Analyzer:
    """
    Analyzers are run against images to update the information we hold about
    them (this information is added to their meta data).
    """

    def __init__(self, name, **kwargs):

        # The name of the analyzer
        self._name = name

        # The arguments for the analyzer
        self._args = {k: v for k, v in kwargs.items() if v is not None}

    def to_json_type(self):
        return [self._name, self._args]


from . import images
