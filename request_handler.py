import json
import requests
import urllib3
import logging
from enum import Enum
from dataclasses import dataclass

class RequestTypeEnum(Enum):
    GET_REQUEST = 1
    POST_REQUEST = 2

@dataclass
class ZpoolCapacity:
    ZpoolName: str
    ZpoolAvailableBytes: int
    TotalUsedBytesForAllDatasets: int

class RequestHandler:
    def __init__(self, base_url, user, secret, verify_cert):
        self._base_url = base_url
        self._user = user
        self._secret = secret
        self._verify_cert = verify_cert
        if not verify_cert:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def do_request(self, resource, requestType, optionalPayload=None):
        request_url = f'{self._base_url}/{resource}/'
        logging.debug(f'request_url: {request_url}')
        logging.debug(f'requestType: {requestType}')
        optionalPayloadAsJson = json.dumps(optionalPayload) if optionalPayload else None

        auth = (self._user, self._secret) if self._user else False
        headers = {'Authorization': f'Bearer {self._secret}'} if not self._user else {}

        if requestType is RequestTypeEnum.GET_REQUEST:
            r = requests.get(request_url, auth=auth, headers=headers, data=optionalPayloadAsJson, verify=self._verify_cert)
        elif requestType is RequestTypeEnum.POST_REQUEST:
            r = requests.post(request_url, auth=auth, headers=headers, data=optionalPayloadAsJson, verify=self._verify_cert)
        else:
            sys.exit(f'UNKNOWN - request failed - Unknown RequestType: {requestType}')

        logging.debug(f'response: {r.text}')
        r.raise_for_status()

        return r.json() if r.ok else None

    def get_request(self, resource):
        return self.do_request(resource, RequestTypeEnum.GET_REQUEST)

    def get_request_with_payload(self, resource, optionalPayload):
        return self.do_request(resource, RequestTypeEnum.GET_REQUEST, optionalPayload)

    def post_request(self, resource):
        return self.do_request(resource, RequestTypeEnum.POST_REQUEST)

    def post_request_with_payload(self, resource, optionalPayload):
        return self.do_request(resource, RequestTypeEnum.POST_REQUEST, optionalPayload)
