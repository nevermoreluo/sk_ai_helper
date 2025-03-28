
import requests.compat
from utils.sklogger import logger
import requests


class SkHttpResponse:
    def __init__(self, status_code: int, content: str, json: dict=None):
        """
        Initialize an SkHttpResponse instance.

        :param status_code: The HTTP status code of the response.
        :param content: The content of the response as a string.
        :param json: An optional dictionary representing the JSON content of the response.
        """
        self.status_code = status_code
        self.content = content
        self.json = json

    def __str__(self):
        """
        Return a string representation of the SkHttpResponse instance.

        :return: A string containing the HTTP status code, content, and optionally JSON data.
        """
        return f"status_code: {self.status_code}, content: {self.content}, json: {self.json}"


class SkHttpClient:
    def __init__(self, host: str):
        """
        Initialize an HttpHelper instance.

        This method creates a new requests.Session instance, which is used to
        send all HTTP requests. This allows the session to persist certain
        parameters across requests, such as cookies and headers.

        """
        self.session = requests.Session()
        self.host = host
    
    def _get(self, url: str, json_data: dict|None = None, **kwargs) -> requests.Response:
        """
        Send an HTTP GET request to the specified URL.

        This method sends an HTTP GET request to the specified URL and
        returns the response. If the response status code is 400 or greater,
        an error message is logged.

        :param url: The URL to send the request to.
        :param json_data: An optional dictionary containing JSON data to
            send with the request.
        :param kwargs: Additional keyword arguments to pass to the
            requests.Session.get method.
        :return: The HTTP response.
        """
        url = requests.compat.urljoin(self.host, url)
        resp = self.session.get(url, json=json_data, **kwargs)
        if resp.status_code >= 400:
            logger.error(f"Request {url}, {json_data},\
                          failed with status code {resp.status_code}, resp: {resp.content}")
        return resp
    
    def get(self, url: str, json_data = None, **kwargs) -> SkHttpResponse:
        """
        Send an HTTP GET request to the specified URL.

        This method sends an HTTP GET request using the internal _get method
        and returns an SkHttpResponse object. If the response status code is 400
        or greater, an error message is logged.

        :param url: The URL to send the request to.
        :param json_data: An optional dictionary containing JSON data to
            send with the request.
        :param kwargs: Additional keyword arguments to pass to the
            requests.Session.get method.
        :return: An SkHttpResponse object containing the status code and content.
        """
        resp =  self._get(url, json=json_data,  **kwargs)
        return SkHttpResponse(resp.status_code, resp.content)

    def get_json(self, url, json_data = None, **kwargs) -> SkHttpResponse:
        """
        Send an HTTP GET request to the specified URL and return a JSON response.

        This method sends an HTTP GET request using the internal _get method and
        returns an SkHttpResponse object. If the response status code is 400 or greater,
        an error message is logged.

        :param url: The URL to send the request to.
        :param json_data: An optional dictionary containing JSON data to
            send with the request.
        :param kwargs: Additional keyword arguments to pass to the
            requests.Session.get method.
        :return: An SkHttpResponse object containing the status code, content, and JSON data.
        """
        resp =  self._get(url, json=json_data,  **kwargs)
        return SkHttpResponse(resp.status_code, resp.content, resp.json())

    def _post(self, url: str, json: dict|None=None, **kwargs) -> requests.Response:
        url = requests.compat.urljoin(self.host, url)
        resp = self.session.post(url, json=json, **kwargs)
        if resp.status_code >= 400:
            logger.error(f"Request {url}, {json}, \
                          failed with status code {resp.status_code}, resp: {resp.content}")
        return resp

    def post(self, url: str, json: dict|None=None, **kwargs) -> SkHttpResponse:
        """
        Send an HTTP POST request to the specified URL.

        This method sends an HTTP POST request using the internal _post method
        and returns an SkHttpResponse object. If the response status code is 400
        or greater, an error message is logged.

        :param url: The URL to send the request to.
        :param json: An optional dictionary containing JSON data to
            send with the request.
        :param kwargs: Additional keyword arguments to pass to the
            requests.Session.post method.
        :return: An SkHttpResponse object containing the status code and content.
        """
        resp =  self._post(url, json=json, **kwargs)
        return SkHttpResponse(resp.status_code, resp.content)
    
    def post_json(self, url: str, json: dict|None=None, **kwargs) -> SkHttpResponse:
        """
        Send an HTTP POST request to the specified URL and return a JSON response.

        This method sends an HTTP POST request using the internal _post method and
        returns an SkHttpResponse object. If the response status code is 400 or greater,
        an error message is logged.

        :param url: The URL to send the request to.
        :param json: An optional dictionary containing JSON data to
            send with the request.
        :param kwargs: Additional keyword arguments to pass to the
            requests.Session.post method.
        :return: An SkHttpResponse object containing the status code, content, and JSON data.
        """
        resp =  self._post(url, json=json, **kwargs)
        return SkHttpResponse(resp.status_code, resp.content, resp.json())
    

