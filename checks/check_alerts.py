import sys

def check_alerts(request_handler, ignore_dismissed_alerts):
    alerts = request_handler.get_request('alert/list')
    warn, crit = 0, 0
    critical_messages, warning_messages = '', ''

    for alert in alerts:
        if ignore_dismissed_alerts and alert['dismissed']:
            continue
        if alert['level'] == 'CRITICAL':
            crit += 1
            critical_messages += "- (C) " + alert['formatted'].replace('\n', '. ') + " "
        elif alert['level'] == 'WARNING':
            warn += 1
            warning_messages += "- (W) " + alert['formatted'].replace('\n', '. ') + " "

    if crit > 0:
        print(f'CRITICAL {critical_messages} {warning_messages}')
        sys.exit(2)
    elif warn > 0:
        print(f'WARNING {warning_messages}')
        sys.exit(1)
    else:
        print('OK - No problem alerts')
        sys.exit(0)
