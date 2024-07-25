#!/usr/bin/env python3

import sys
import argparse
from startup import Startup
from config import check_truenas_script_version, default_zpool_warning_percent, default_zpool_critical_percent

def main():
    parser = argparse.ArgumentParser(description=f'Checks a TrueNAS/FreeNAS server using the 2.0 API. Version {check_truenas_script_version}')
    parser.add_argument('-H', '--hostname', required=True, type=str, help='Hostname or IP address')
    parser.add_argument('-u', '--user', type=str, help='Username, only root works, if not specified: use API Key')
    parser.add_argument('-p', '--passwd', required=True, type=str, help='Password or API Key')
    parser.add_argument('-t', '--type', required=True, type=str, help='Type of check, either alerts, zpool, zpool_capacity, repl, or update')
    parser.add_argument('-pn', '--zpoolname', type=str, default='all', help='For check type zpool, the name of zpool to check. Optional; defaults to all zpools.')
    parser.add_argument('-ns', '--no-ssl', action='store_true', help='Disable SSL (use HTTP); default is to use SSL (use HTTPS)')
    parser.add_argument('-nv', '--no-verify-cert', action='store_true', help='Do not verify the server SSL cert; default is to verify the SSL cert')
    parser.add_argument('-ig', '--ignore-dismissed-alerts', action='store_true', help='Ignore alerts that have already been dismissed in FreeNas/TrueNAS; default is to treat them as relevant')
    parser.add_argument('-d', '--debug', action='store_true', help='Display debugging information; run script this way and record result when asking for help.')
    parser.add_argument('-zw', '--zpool-warn', type=int, default=default_zpool_warning_percent, help=f'ZPool warning storage capacity free threshold. Give a percent value in the range 1-100, defaults to {default_zpool_warning_percent}%%. Used with zpool_capacity check.')
    parser.add_argument('-zc', '--zpool-critical', type=int, default=default_zpool_critical_percent, help=f'ZPool critical storage capacity free threshold. Give a percent value in the range 1-100, defaults to {default_zpool_critical_percent}%%. Used with zpool_capacity check.')
    parser.add_argument('-zp', '--zpool-perfdata', action='store_true', help='Add Zpool capacity perf data to output. Used with zpool_capacity check.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(sys.argv[1:])
    use_ssl = not args.no_ssl
    verify_ssl_cert = not args.no_verify_cert

    startup = Startup(args.hostname, args.user, args.passwd, use_ssl, verify_ssl_cert, args.ignore_dismissed_alerts, args.debug, args.zpoolname, args.zpool_warn, args.zpool_critical, args.zpool_perfdata)
    startup.handle_requested_alert_type(args.type)

if __name__ == '__main__':
    main()
