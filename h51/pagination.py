
# NOTE: The `Page` classes provides a thin wrapper to paginated data fetched
# from the  API by the API client, it should not be  initialized directly.


class Page:

    def __init__(self, results, result_count, url, has_more):

        # The results within the page
        self._results = results

        # The total number of results available
        self._result_count = result_count

        # The URL used to fetch the results
        self._url = url

        # A flag indicating if there are more results after this page of
        # results.
        self._has_more = has_more

    def __getitem__(self, i):
        return self._results[i]

    def __iter__(self):
        for result in self._results:
            yield result

    def __len__(self):
        return len(self._results)

    @property
    def has_more(self):
        return self._has_more

    @property
    def result_count(self):
        return self._has_more

    @property
    def results(self):
        return list(self._results)

    @property
    def url(self):
        return list(self._url)
