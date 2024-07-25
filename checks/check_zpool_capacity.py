import sys
from request_handler import ZpoolCapacity

def check_zpool_capacity(request_handler, zpool_name, zpool_warn, zpool_critical, show_zpool_perfdata):
    BYTES_IN_MEGABYTE = 1024 * 1024
    datasetPayload = {'query-options': {'extra': {'flat': False}}, 'query-filters': []}
    dataset_results = request_handler.get_request_with_payload('pool/dataset', datasetPayload)
    warn, crit = 0, 0
    critical_messages, warning_messages = '', ''
    zpools_examined_with_no_issues = ''
    root_level_datasets_examined = ''
    root_level_dataset_count = 0
    all_root_level_dataset_names = ''
    perfdata = ';|' if show_zpool_perfdata else ''
    looking_for_all_pools = zpool_name.lower() == 'all'
    zpoolNameToCapacityDict = {}

    for dataset in dataset_results:
        root_level_dataset_count += 1
        dataset_name = dataset['name']
        dataset_pool_name = dataset['pool']
        all_root_level_dataset_names += f'{dataset_name} '

        if looking_for_all_pools or zpool_name == dataset_pool_name:
            root_level_datasets_examined += f' {dataset_name}'
            dataset_used_bytes = dataset['used']['parsed']
            dataset_available_bytes = dataset['available']['parsed']

            if dataset_pool_name not in zpoolNameToCapacityDict:
                newZpoolCapacity = ZpoolCapacity(dataset_pool_name, dataset_available_bytes, dataset_used_bytes)
                zpoolNameToCapacityDict[dataset_pool_name] = newZpoolCapacity
            else:
                zpoolNameToCapacityDict[dataset_pool_name].TotalUsedBytesForAllDatasets += dataset_used_bytes

            if show_zpool_perfdata:
                total_bytes = dataset_used_bytes + dataset_available_bytes
                used_percentage = (dataset_used_bytes / total_bytes) * 100
                perfdata += f" {dataset_name}={dataset_used_bytes}B;{used_percentage:.2f}%;{dataset_available_bytes}B;{total_bytes}B"

    for currentZpoolCapacity in zpoolNameToCapacityDict.values():
        zpoolTotalBytes = currentZpoolCapacity.ZpoolAvailableBytes + currentZpoolCapacity.TotalUsedBytesForAllDatasets
        usedPercentage = (currentZpoolCapacity.TotalUsedBytesForAllDatasets / zpoolTotalBytes) * 100
        usagePercentDisplayString = f'{usedPercentage:3.1f}'

        if usedPercentage >= zpool_critical:
            crit += 1
            critical_messages += f" - Pool {currentZpoolCapacity.ZpoolName} usage {usagePercentDisplayString}% exceeds critical value of {zpool_critical}%"
        elif usedPercentage >= zpool_warn:
            warn += 1
            warning_messages += f" - Pool {currentZpoolCapacity.ZpoolName} usage {usagePercentDisplayString}% exceeds warning value of {zpool_warn}%"
        else:
            if zpools_examined_with_no_issues:
                zpools_examined_with_no_issues += ' - '
            zpools_examined_with_no_issues += f"{currentZpoolCapacity.ZpoolName} ({usagePercentDisplayString}% used)"

        if show_zpool_perfdata:
            usedMegabytes = currentZpoolCapacity.TotalUsedBytesForAllDatasets / BYTES_IN_MEGABYTE
            warningBytes = zpoolTotalBytes * (zpool_warn / 100)
            criticalBytes = zpoolTotalBytes * (zpool_critical / 100)
            totalMegabytes = zpoolTotalBytes / BYTES_IN_MEGABYTE
            perfdata += f" {currentZpoolCapacity.ZpoolName}={usedMegabytes:3.2f}MB;{warningBytes/BYTES_IN_MEGABYTE:3.2f};{criticalBytes/BYTES_IN_MEGABYTE:3.2f};0;{totalMegabytes:3.2f}"

    if root_level_datasets_examined == '' and root_level_dataset_count == 0 and looking_for_all_pools:
        root_level_datasets_examined = '(No Datasets found)'

    if root_level_datasets_examined == '' and root_level_dataset_count > 0 and not looking_for_all_pools and crit == 0:
        crit += 1
        critical_messages += f'- No datasets found matching ZPool {zpool_name} out of {root_level_dataset_count} root level datasets ({all_root_level_dataset_names})'

    if crit > 0:
        print(f'CRITICAL {critical_messages} {warning_messages} - {zpools_examined_with_no_issues}{perfdata}')
        sys.exit(2)
    elif warn > 0:
        print(f'WARNING {warning_messages} - {zpools_examined_with_no_issues}{perfdata}')
        sys.exit(1)
    else:
        print(f'OK - No Zpool capacity issues. ZPools examined: {zpools_examined_with_no_issues} - Root level datasets examined: {root_level_datasets_examined}{perfdata}')
        sys.exit(0)
