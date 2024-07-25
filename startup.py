import logging
from utils import setup_logging
from checks.check_alerts import check_alerts
import sys
import os
import logging
import requests

class RequestHandler:
    def __init__(self, base_url, user, secret, verify_cert):
        self.base_url = base_url
        self.auth = (user, secret)
        self.verify_cert = verify_cert

    def get(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.get(url, auth=self.auth, verify=self.verify_cert)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f'Error making GET request to {url}: {e}')
            raise

    def post(self, endpoint, data):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.post(url, json=data, auth=self.auth, verify=self.verify_cert)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f'Error making POST request to {url}: {e}')
            raise

from checks.check_alerts import check_alerts
from checks.check_repl import check_repl
from checks.check_update import check_update
from checks.check_zpool import check_zpool
from checks.check_zpool_capacity import check_zpool_capacity
from utils import setup_logging

class Startup:
    def __init__(self, hostname, user, secret, use_ssl, verify_cert, ignore_dismissed_alerts, debug_logging, zpool_name, zpool_warn, zpool_critical, show_zpool_perfdata):
        self._hostname = hostname
        self._user = user
        self._secret = secret
        self._use_ssl = use_ssl
        self._verify_cert = verify_cert
        self._ignore_dismissed_alerts = ignore_dismissed_alerts
        self._debug_logging = debug_logging
        self._zpool_name = zpool_name
        self._wfree = zpool_warn
        self._cfree = zpool_critical
        self._show_zpool_perfdata = show_zpool_perfdata

        http_request_header = 'https' if use_ssl else 'http'
        self._base_url = f'{http_request_header}://{hostname}/api/v2.0'

        setup_logging(debug_logging)
        self.log_startup_information()
        self.log_startup_information()

        self.request_handler = RequestHandler(self._base_url, user, secret, verify_cert)

    def log_startup_information(self):
        logging.debug(f'hostname: {self._hostname}')
        logging.debug(f'use_ssl: {self._use_ssl}')
        logging.debug(f'verify_cert: {self._verify_cert}')
        logging.debug(f'base_url: {self._base_url}')
        logging.debug(f'zpool_name: {self._zpool_name}')
        logging.debug(f'wfree: {self._wfree}')
        logging.debug(f'cfree: {self._cfree}')
        setup_logging(self._debug_logging)

    def handle_requested_alert_type(self, alert_type):
        # Implementation for handling different alert types
        pass

# Example of setting up logging configuration
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Load configuration from environment variables or a config file
    hostname = os.getenv('HOSTNAME')
    user = os.getenv('USER')
    secret = os.getenv('SECRET')
    use_ssl = os.getenv('USE_SSL', 'false').lower() == 'true'
    verify_cert = os.getenv('VERIFY_CERT', 'true').lower() == 'true'
    ignore_dismissed_alerts = os.getenv('IGNORE_DISMISSED_ALERTS', 'false').lower() == 'true'
    debug_logging = os.getenv('DEBUG_LOGGING', 'false').lower() == 'true'
    zpool_name = os.getenv('ZPOOL_NAME')
    zpool_warn = int(os.getenv('ZPOOL_WARN', '80'))
    zpool_critical = int(os.getenv('ZPOOL_CRITICAL', '90'))
    show_zpool_perfdata = os.getenv('SHOW_ZPOOL_PERFDATA', 'false').lower() == 'true'

    startup = Startup(hostname, user, secret, use_ssl, verify_cert, ignore_dismissed_alerts, debug_logging, zpool_name, zpool_warn, zpool_critical, show_zpool_perfdata)

