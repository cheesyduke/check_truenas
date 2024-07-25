import sys

def check_repl(request_handler):
    repls = request_handler.get_request('replication')
    errors = 0
    msg = ''
    replications_examined = ''

    for repl in repls:
        repl_name = repl['name']
        repl_state_code = repl['state']['state']
        replications_examined += f' {repl_name}: {repl_state_code}'
        if repl_state_code not in ['FINISHED', 'RUNNING']:
            errors += 1
            msg += f'{repl_name}: {repl_state_code} '

    if errors > 0:
        print(f'WARNING - There are {errors} replication errors [{msg.strip()}]. Go to Storage > Replication Tasks > View Replication Tasks in TrueNAS for more details.')
        sys.exit(1)
    else:
        print(f'OK - No replication errors. Replications examined: {replications_examined}')
        sys.exit(0)
