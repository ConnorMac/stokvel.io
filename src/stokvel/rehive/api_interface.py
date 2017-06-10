""" Python api for Rehive """
import os
import requests
import json


class ApiInterface:
    """
    Interface for interacting with the rehive api
    """
    API_ENDPOINT = os.environ.get("REHIVE_API_V3_URL", 
                                  "https://rehive.com/api/3/")

    def __init__(self, token=None, connection_pool_size=0, API_ENDPOINT=API_ENDPOINT):
        self.token = token
        self.endpoint = API_ENDPOINT
        self._connection_pool_size = connection_pool_size
        self._session = None

    def post(self, path, data):
        return self._request('post', path, data)

    def get(self, path):
        return self._request('get', path)

    def put(self, path, data):
        return self._request('put', path, data)

    def patch(self, path, data):
        return self._request('patch', path, data)

    def delete(self, path, data):
        return self._request('delete', path)

    def _create_session(self):
        self._session = requests.Session()
        if self._connection_pool_size > 0:
            adapter = requests.adapters.HTTPAdapter(pool_connections=self._connection_pool_size,
                                                    pool_maxsize=self._connection_pool_size)
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)

    def _request(self, method, path, data=None):
        if self._session is None:
            self._create_session()

        url = self.API_ENDPOINT + path
        headers = self._get_headers()

        # TODO Proper exception handling
        try:
            if data:
                try:
                    data = json.dumps(data)
                except:
                    raise
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               data=data)
            else:
                result = self._session.request(method, url, headers=headers)

            if (result.status_code != 200 and result.status_code != 201):
                try:
                    data = result.json()
                    raise Exception(data['message'])
                except:
                    raise Exception('General error')

            response_json = self._handle_result(result)
            return response_json

        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to Rehive.")
        except requests.exceptions.Timeout:
            raise eException("Connection timed out.")
        except ValueError:
            if result:
                raise ValueError(result.text)
            else:
                raise
        except KeyError:
            if result:
                raise KeyError(result.text)
            else:
                raise

    def _handle_result(self, result):
        json = result.json()

        # Check for token in response and set it for the current object
        if (json and 'data' in json and 'token' in json['data']):
            self._set_token = json['data']['token']
        
        data = {
            'http_code': result.status_code,
        }
        data['data'] = json['data']

        return data

    def _set_token(token):
        self.token = token

    def _get_headers(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        if self.token is not None:
            headers['Authorization'] = 'Token ' + str(self.token)

        return headers