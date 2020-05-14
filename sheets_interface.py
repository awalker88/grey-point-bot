import pygsheets as pyg

client = pyg.authorize()
workbook = client.open('Grey Points')

tst = workbook.worksheet_by_title('test')
