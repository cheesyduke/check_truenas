import sys

def check_update(request_handler):
    updateCheckResult = request_handler.post_request('update/check_available')
    updateCheckResultDict = {
        'UNAVAILABLE': 'no update available',
        'AVAILABLE': 'an update is available',
        'REBOOT_REQUIRED': 'an update has already been applied',
        'HA_UNAVAILABLE': 'HA is non-functional'
    }

    updateCheckResultString = updateCheckResult['status']
    needsUpdateOrOtherPossibleIssue = updateCheckResultString != 'UNAVAILABLE'

    if needsUpdateOrOtherPossibleIssue:
        status_message = updateCheckResultDict.get(updateCheckResultString, 'Unknown Update Status')
        print(f'WARNING - Update Status: {updateCheckResultString} ({status_message}). Update may be required. Go to TrueNAS Dashboard -> System -> Update to check for newer version.')
        sys.exit(1)
    else:
        print(f'OK - Update Status: {updateCheckResultString} ({updateCheckResultDict[updateCheckResultString]})')
        sys.exit(0)
