record = []
def sheet_api(client_secret):
	'''
	Takes client_secret as argument. Uses google sheets api to fetch entire sheet. 
	returns two things: addresses, ids. addresses is a list of metro stations. ids is a list of 4-tuples 
	a 4-tuple contains (name, contact, alt contact, blood group)
	'''
	client_secret = client_secret.strip("'").strip('"')
	import gspread
	from oauth2client.service_account import ServiceAccountCredentials
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	with open("./temp.json", "w") as a:
		a.write(client_secret)
	creds = ServiceAccountCredentials.from_json_keyfile_name('temp.json', scope)
	with open("./temp.json", "w") as a:
		a.write("this file is used temporarily for storing client secret for a teeny tiny amount of time because \
			gspread won't authorize without a file.")
	#creds = ServiceAccountCredentials.from_json(client_secret)
	client = gspread.authorize(creds)
	sheets = client.open('Copy of Blood Donation (Responses)')
	sheet_0 = sheets.worksheet("Sheet 0")
	sheet_1 = sheets.worksheet("Sheet 1")
	global record 
	record = sheet_0.get_all_records()+sheet_1.get_all_records()
	#print(record[0].keys())#all fields
	addresses = []
	ids = []
	for row in record:
		n_i   = row["Name"]
		c_i_1 = row["Contact Number"]
		c_i_2 = row["Alternate Contact Number"]
		b_i   = row["Blood Group"]
		m_i   = row["Metro Station"]
		addresses.append(m_i)
		ids.append((n_i, c_i_1, c_i_2, b_i))
	return addresses, ids
	#record = sheet.row_values(2)
	#record = sheet.col_values(2)
	#record = sheet.cell(2, 2).value()
	#sheet.update_cell(2, 2, 'new-val')
	#sheet.delete_row(row, index)
	#sheet.insert_row(row, index)
	#print(sheet.row_count)
	