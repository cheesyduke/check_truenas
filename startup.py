import logging
from request_handler import RequestHandler
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

        self.request_handler = RequestHandler(self._base_url, user, secret, verify_cert)

    def log_startup_information(self):
        logging.debug(f'hostname: {self._hostname}')
        logging.debug(f'use_ssl: {self._use_ssl}')
        logging.debug(f'verify_cert: {self._verify_cert}')
        logging.debug(f'base_url: {self._base_url}')
        logging.debug(f'zpool_name: {self._zpool_name}')
        logging.debug(f'wfree: {self._wfree}')
        logging.debug(f'cfree: {self._cfree}')

    def handle_requested_alert_type(self, alert_type):
        if alert_type == 'alerts':
            check_alerts(self.request_handler, self._ignore_dismissed_alerts)
        elif alert_type == 'repl':
            check_repl(self.request_handler)
        elif alert_type == 'update':
            check_update(self.request_handler)
        elif alert_type == 'zpool':
            check_zpool(self.request_handler, self._zpool_name)
        elif alert_type == 'zpool_capacity':
            check_zpool_capacity(self.request_handler, self._zpool_name, self._wfree, self._cfree, self._show_zpool_perfdata)
        else:
            sys.exit(f"Unknown type: {alert_type}")

