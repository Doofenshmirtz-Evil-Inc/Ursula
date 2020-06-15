''' user account manager for ursulaListener '''

import logging
from datetime import datetime
from pathlib import Path
from random import choice

import gspread
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(name)s | %(message)s'))
logger = logging.getLogger('accountManager')
logger.setLevel('DEBUG')

# sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(str(Path(__file__).resolve().parents[0]) + '/creds.json', scope)


def getAccount():
    '''
    returns a random available account token and if its a bot or not 
    returns in format str accountToken, bool isBot
    '''

    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key('1sW1EWWTYz-vQKuJQ6thJ8Fstm4IdtwpntauruiH3uU0').sheet1
    accounts = sheet.get_all_values()[1:]

    accountsAvailable = []

    for account in accounts:
        if account[1] == '':
            account[1] = str(datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
        
        accountLastLoggedTime = datetime.strptime(account[1], "%m-%d-%Y %H:%M:%S").timestamp()
        distance = datetime.now().timestamp() - accountLastLoggedTime # the amount of time in seconds since the last time this account was logged in
        if account[1].lower() == 'false' or distance > 1800: # if this account hasnt been used in 30 mins
            accountsAvailable.append(account)

    # grab the account and token
    logger.debug(f'found {len(accountsAvailable)} available accounts, choosing randomly')
    accountChosen = choice(accountsAvailable)
    logger.debug(accountChosen)
    token = accountChosen[0]

    # check if account is bot
    if accountChosen[2].lower() == 'false':
        isBot = False
    else:
        isBot = True
    
    # upload updated info to sheet
    accountChosenCell = sheet.find(token)
    sheet.update_cell(accountChosenCell.row, accountChosenCell.col, str(datetime.now().strftime("%m-%d-%Y %H:%M:%S")))

    return [token, isBot]

if __name__ == "__main__":
    getAccount()
