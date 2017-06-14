class APIEndpoint(object):
    def __init__(self, client, endpoint, filters=None):
        self.client = client
        self.endpoint = endpoint
        self.filters = filters

    def get(self, function=None):
        url = self._build_url(function)
        response = self.client.get(url)
        return response

    def post(self, data, function=None):
        url = self._build_url(function)
        response = self.client.post(url, data)
        return response

    # PRIVATE METHODS
    def _build_url(self, function=None):
        endpoint = self.endpoint + function if function else self.endpoint
        url = endpoint + self.filters if self.filters else endpoint
        return url


class APIList(APIEndpoint):

    def __init__(self, client, endpoint, filters=None):
        super(APIList, self).__init__(client, endpoint, filters)
        self.next = None
        self.previous = None
        self.count = 0

    def get(self, endpoint=None):
        response = super().get(endpoint)
        self._set_pagination(response)
        return response

    def get_next(self):
        url = self._build_pagination_url(self.next)
        response = self.client.get(url)
        self._set_pagination(response)
        return response

    def get_previous(self):
        url = self._build_pagination_url(self.previous)
        response = self.client.get(url)
        self._set_pagination(response)
        return response

    # PRIVATE METHODS
    def _set_pagination(self, response):
        data = response.get('data')
        if 'next' in data:
            if data.get('next') is not None:
                self.next = self._get_next_page_filter(data.get('next'))
            else:
                self.next = data.get('next')
        if 'previous' in data:
            if data.get('previous') is not None:
                self.previous = self._get_next_page_filter(data['previous'])
            else:
                self.previous = data.get('previous')
        if 'count' in data:
            self.count = data.get('count')

    def _get_next_page_filter(self, string):
        url_segments = string.split('/')
        last_segment = url_segments[-1]
        return last_segment

    def _build_pagination_url(self, pagination, function=None):
        endpoint = self.endpoint + function if function else self.endpoint
        paginatated_endpoint = endpoint + pagination
        if self.filters:
            paginatated_endpoint = paginatated_endpoint + self.filters
        return paginatated_endpoint
