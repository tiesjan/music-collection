from json.decoder import JSONDecodeError
from urllib.parse import urljoin

import requests


class DiscogsAPIClientAuth(requests.auth.AuthBase):
    """
    Authentication class used for authenticating requests using required
    Discogs API access token.
    """
    def __init__(self, access_token):
        """
        DiscogsAPIClientAuth initializer.

        Parameters:
          access_token   Discogs API access token
        """
        self.access_token = access_token

    def __call__(self, request):
        """
        Modifies the given request by adding an Authorization header with the
        Discogs API access token.
        """
        access_token_header = "Discogs token={}".format(self.access_token)
        request.headers["Authorization"] = access_token_header
        return request


class DiscogsAPIRequestException(Exception):
    """
    Exception type raised when an error is encountered in DiscogsAPIClient.
    """
    pass


class DiscogsAPIClient(object):

    BASE_URL = "https://api.discogs.com/"

    def __init__(self, access_token, max_tries=3, timeout=(2, 30)):
        """
        DiscogsAPIClient initializer.

        Parameters:
          access_token   Discogs API access token
          max_tries      max number of connection tries
          timeout        tuple of (connect timeout, read timeout), in seconds
        """
        self.access_token = access_token
        self.timeout = timeout

        # Mount customly configured HTTPAdapter
        self.session = requests.Session()
        http_adapter = requests.adapters.HTTPAdapter(max_retries=max_tries - 1)
        self.session.mount("https://", http_adapter)
        self.session.mount("http://", http_adapter)

    # Private helper to perform requests
    def _request(self, method, endpoint, params=None, json=None):
        # Prepare request requirements
        authenticator = DiscogsAPIClientAuth(self.access_token)
        headers = {
            "Accept": "application/vnd.discogs.v2.discogs+json",
            "User-Agent": "TJCompilationEnhancer/0.9",
        }
        url = urljoin(self.BASE_URL, endpoint)

        # Perform request
        try:
            response = self.session.request(method, url, auth=authenticator,
                    headers=headers, timeout=self.timeout, params=params,
                    json=json)
        except requests.RequestException as exception:
            message = "[{}] {}".format(type(exception).__name__, exception)
            raise DiscogsAPIRequestException(message)

        # Handle responses with statuses in 4xx and 5xx range
        try:
            response.raise_for_status()
        except requests.HTTPError as exception:
            message = "[{}] {} -- {}".format(
                    type(exception).__name__, exception, exception.response.text)
            raise DiscogsAPIRequestException(message)

        # Parse response as JSON and return result
        try:
            return response.json()
        except JSONDecodeError as exception:
            message = "Error decoding JSON: {}. Response was: {}".format(
                    exception, response.text)
            raise DiscogsAPIRequestException(message)

    def get_release(self, discogs_release_id):
        """
        Retrieves information on the Discogs release with the given id.
        """
        method = "GET"
        endpoint = "/releases/{}".format(discogs_release_id)

        try:
            return self._request(method, endpoint)
        except DiscogsAPIRequestException as exception:
            message = "Could not retrieve Discogs release info"
            raise DiscogsAPIRequestException("{}: {}".format(message, exception))
