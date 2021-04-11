from datetime import timedelta, datetime

import requests

from . import constants
from .settings import CLIENT_SECRET, CLIENT_KEY


class Client:
    def __init__(self):
        self.authorization_token = None
        self.AUTHORIZATION_EXPIRY_TIME = None

    def _get_headers(self, content_type='application/json', include_auth_header=True):
        if content_type:
            headers = {
                'Content-type': content_type
            }
        else:
            headers = {}

        headers.update(self._get_application_header())

        if include_auth_header:
            headers.update(self._get_authorization_header())

        return headers

    def _get_application_header(self):
        headers = {
            constants.APPLICATION_HEADER: CLIENT_KEY
        }

        return headers

    def _get_authorization_header(self):
        headers = {}

        if CLIENT_SECRET:
            if (
                not self.authorization_token or
                self.authorization_expiry_time < datetime.now()
            ):
                self._obtain_authorization_token()

            headers[constants.AUTHORIZATION_HEADER] = "{bearer} {token}".format(
                bearer=constants.AUTHORIZATION_BEARER,
                token=self.authorization_token
            )

        return headers

    def _obtain_authorization_token(self):
        if CLIENT_SECRET:
            request_headers = self._get_application_header()

            request_headers[constants.AUTHORIZATION_HEADER] = "{bearer} {token}".format(
                bearer=constants.CREDENTIAL_BEARER,
                token=CLIENT_SECRET
            )

            request_body = {
                'grant_type': constants.CREDENTIAL_GRAT_TYPE
            }

            response = requests.post(
                constants.V_1_0_AUTHORIZATION_TOKEN_ENDPOINT,
                headers=request_headers,
                data=request_body
            )

            if response.status_code == 200:
                self.authorization_token = response.json().get('authorization_token')
                self.authorization_expiry_time = datetime.now() + timedelta(
                    seconds=constants.AUTHORIZATION_TOKEN_TIMEOUT
                )

            elif response.status_code in [400, 401, 403]:
                # TODO handle errors properly
                raise Exception(response.json().get('errors'))

    def post(self, endpoint, body, include_auth_header=True, customer_headers={}):
        headers = self._get_headers(
            include_auth_header=include_auth_header)

        response = requests.post(
            url=endpoint,
            headers=headers,
            json=body
        )

        return response
