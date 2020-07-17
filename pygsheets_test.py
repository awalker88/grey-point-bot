import pygsheets as pyg
from time import sleep


print(':::started')
client = pyg.authorize(
    service_account_env_var='sheet_client_secret_json'
)
print(':::authorized')
while True:
    workbook = client.open('Grey Points')
    print('workbook:::', workbook)
    sleep(3)
