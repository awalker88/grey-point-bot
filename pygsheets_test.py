import pygsheets as pyg

client = pyg.authorize(
    service_account_env_var='sheet_client_secret_json'
)

workbook = client.open('Grey Points')
print('workbook:::', workbook)
