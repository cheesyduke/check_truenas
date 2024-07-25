import sys

def check_zpool(request_handler, zpool_name):
    pool_results = request_handler.get_request('pool')
    warn, crit = 0, 0
    critical_messages, warning_messages = '', ''
    zpools_examined = ''
    actual_zpool_count = 0
    all_pool_names = ''
    looking_for_all_pools = zpool_name.lower() == 'all'

    for pool in pool_results:
        actual_zpool_count += 1
        pool_name = pool['name']
        pool_status = pool['status']
        all_pool_names += f'{pool_name} '

        if looking_for_all_pools or zpool_name == pool_name:
            zpools_examined += f' {pool_name}'
            if pool_status != 'ONLINE':
                crit += 1
                critical_messages += f'- (C) ZPool {pool_name} is {pool_status}'

    if zpools_examined == '' and actual_zpool_count == 0 and looking_for_all_pools:
        zpools_examined = '(None - No Zpools found)'

    if zpools_examined == '' and actual_zpool_count > 0 and not looking_for_all_pools and crit == 0:
        crit += 1
        critical_messages += f'- No Zpools found matching {zpool_name} out of {actual_zpool_count} pools ({all_pool_names})'

    if crit > 0:
        print(f'CRITICAL {critical_messages} {warning_messages}')
        sys.exit(2)
    elif warn > 0:
        print(f'WARNING {warning_messages}')
        sys.exit(1)
    else:
        print(f'OK - No problem Zpools. Zpools examined: {zpools_examined}')
        sys.exit(0)
