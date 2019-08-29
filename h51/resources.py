
from datetime import datetime

from . import pagination


# NOTE: The `Asset`, `PartialAsset` and `Variation` classes provide thin
# wrappers to data fetched from the API by the API client. They should not be
# initialized directly. Instead they should be returned by class methods such
# as `create`, `all`, `one` and `many`.


class _BaseResource:
    """
    A base resource used to wrap documents fetched from the API with dot
    notation access to attributes and methods for access to related API
    endpoints.
    """

    def __init__(self, client, document):

        # The API client used to fetch the resource
        self._client = client

        # The document representing the resource's data
        self._document = document

    def __getattr__(self, name):

        if '_document' in self.__dict__:
            return self.__dict__['_document'].get(name, None)

        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}'"
        )

    def __getitem__(self, name):
        return self.__dict__['_document'][name]

    def __contains__(self, name):
        return name in self.__dict__['_document']

    def get(self, name, default=None):
        return self.__dict__['_document'].get(name, default)


class PartialAsset(_BaseResource):
    """
    A partial view on an asset on Hangar51.

    NOTE: Partial assets are returned when requesting a list of assets from
    the API. You can expand a partial asset to a full asset by calling the
    `expand` method.
    """

    def __init__(self, client, document):
        super().__init__(client, document)

        # Convert `created` and `modified` to dates
        self._document['created'] \
                = datetime.fromisoformat(self._document['created'])

        self._document['modified'] \
                = datetime.fromisoformat(self._document['modified'])

    def __str__(self):
        return f'Partial asset: {self.uid}'

    def expand(self):
        """Return a full Asset for the partial asset"""
        return self._client.get_asset(self.uid)


class Asset(_BaseResource):
    """
    An asset stored on Hangar51.
    """

    def __init__(self, client, document):
        super().__init__(client, document)

        # Convert `created` and `modified` to dates
        self._document['created'] \
                = datetime.fromisoformat(self._document['created'])

        self._document['modified'] \
                = datetime.fromisoformat(self._document['modified'])

        # Convert variations to `Variation` instances
        if self.get('variations'):
            self._document['variations'] = {
                n: Variation(self._client, self, n, v)
                for n, v in self.variations.items()
            }

        else:
            self.variations = {}

    def __str__(self):
        return f'Asset: {self.uid}'

    def analyze(self, analyzers, notification_url=None):
        """Analyze the asset"""

        r = self._client(
            'post',
            f'assets/{self.uid}/analyze',
            params={'notification_url': notification_url},
            json_type_body=[a.to_json_type() for a in analyzers]
        )

        if not notification_url:
            self.meta = r['meta']

    def download(self):
        """Download the asset"""
        return self._client(
            'get',
            f'assets/{self.uid}/download',
            download=True
        )

    def expire(self, seconds):
        """Set an expires time for the asset"""

        if isinstance(seconds, datetime):
            seconds = datetime.timestamp() - time.time()

        r = self._client(
            'post',
            f'assets/{self.uid}/expire',
            data={'seconds': seconds}
        )

        self._document.update(r)

    def persist(self):
        """Set the asset to persist (remove the expires time)"""

        r = self._client(
            'post',
            f'assets/{self.uid}/persist'
        )

        self._document.update(r)

    @classmethod
    def all(self, client, secure=None, type=None, q=None, rate_buffer=0):
        """
        Get all assets.

        Setting the `rate_buffer` to a value greater than 0 ensures the method
        will wait before continuing to fetch results if the number of
        remaining requests falls below the given rate buffer.
        """

        assets = []
        after = None
        has_more = True
        while has_more:

            # Fetch a page of results
            r = client(
                'get',
                'assets',
                params={
                    'secure': secure,
                    'type': type,
                    'q': q,
                    'after': after,
                    'limit': 100
                }
            )
            assets.extend([PartialAsset(client, a) for a in r['results']])
            after = assets[-1].uid
            has_more = r['has_more']

            if has_more and client.rate_limit_remaining <= rate_buffer:

                # Wait for the rate limit to be reset before requesting
                # another page.
                time.sleep(time.time() - client.rate_limit_reset)

        return assets

    @classmethod
    def create(cls, client, file, name=None, expire=None, secure=False):
        """Upload an asset to Hangar51"""
        return cls(
            client,
            client(
                'put',
                f'assets',
                files={'file': file},
                data={
                    'name': name,
                    'expire': expire,
                    'secure': True if secure else None
                }
            )
        )

    @classmethod
    def many(
        cls,
        client,
        secure=None,
        type=None,
        q=None,
        before=None,
        after=None,
        limit=None
    ):
        """Get a page of assets"""
        r = client(
            'get',
            'assets',
            params={
                'secure': secure,
                'type': type,
                'q': q,
                'before': before,
                'after': after,
                'limit': limit
            }
        )

        return pagination.Page(
            results=[PartialAsset(client, a) for a in r['results']],
            result_count=r['result_count'],
            has_more=r['has_more'],
            url=r['url']
        )

    @classmethod
    def one(cls, client, uid):
        """Return an asset matching the given uid"""
        return cls(client, client('get', f'assets/{uid}'))


class Variation(_BaseResource):
    """
    A variation of an asset
    """

    def __init__(self, client, asset, name, document):

        # The API client used to fetch the variation
        self._client = client

        # The asset the variation belongs to
        self._asset = asset

        # The name of the variation
        self._name = name

        # The document representing the variation's data
        self._document = document

    def __str__(self):
        return f'Variation: {self._name} ({self._asset.uid})'

    def download(self):
        """Download the variation"""
        return self._client(
            'get',
            f'assets/{self._asset.uid}/variations/{self._name}/download',
            download=True
        )

    def delete(self):
        """Delete the variation"""
        self._client(
            'delete',
            f'assets/{self._asset.uid}/variations/{self._name}'
        )
        del self._asset.variations[self._name]

    @classmethod
    def create(cls, asset, variations, notification_url=None):
        """Create a set of variations of the asset"""

        r = asset._client(
            'put',
            f'assets/{asset.uid}/variations',
            params={'notification_url': notification_url},
            json_type_body={
                name: [t.to_json_type() for t in transforms]
                for name, transforms in variations.items()
            }
        )

        if not notification_url:
            asset._document['variations'] = {
                n: cls(asset._client, asset, n, v)
                for n, v in r['variations'].items()
            }
