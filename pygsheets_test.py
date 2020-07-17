import pygsheets as pyg

client = pyg.authorize(
    # service_account_env_var='sheet_client_secret_json' todo: for local
)

workbook = client.open('Grey Points')
print('workbook:::', workbook)