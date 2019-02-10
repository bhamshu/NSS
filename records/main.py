#FIX THE IMPORT THING IN CALL NEAREST:	lol looks like this is the most elegant way to do this. tis some ugliness in python
def builddummycsv(csv_location):
	import csv
	addresses = []
	ids = []
	with open(csv_location) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		skipfirstcolumn = True
		for row in csv_reader:
			if skipfirstcolumn:
				n_i   = row.index("Name")
				c_i_1 = row.index("Contact Number")
				c_i_2 = row.index("Alternate Contact Number")
				b_i   = row.index("Blood Group")
				m_i   = row.index('Nearest Metro Station to Home (Even if you chose "In / Around DTU Campus", choose the metro station nearest to your home if your home is in Delhi)')
				skipfirstcolumn = False
				continue
			addresses.append(row[m_i])
			ids.append((row[n_i], row[c_i_1], row[c_i_2], row[b_i]))
	return addresses, ids


def main(target, blood = None, projectdirpath = ".", client_secret = None):
	if client_secret==None:
		csv_location = projectdirpath+'/dummyresponses.csv'
		addresses, ids = builddummycsv(csv_location)
		del csv_location
	else:
		from spreadsheet import sheet_api
		addresses, ids = sheet_api(client_secret)
		del sheet_api

	name_to_coord = get_metro_coordinates_txt(projectdirpath)
	coord_to_name = {v: k for k, v in name_to_coord.items()}

	d = call_nearest(addresses, target, projectdirpath)
	
	f = open(projectdirpath+"/dump.txt", "w")
	f.write(str(d))
	f.close()
	return d, ids, coord_to_name

def showonterminalinterface(d, ids, coord_to_name):
	i = -1
	sucsex = "n"
	while sucsex == "n" or sucsex == "N":
		i+=1
		if i>=len(d):
			print("\nSorry, out of volunteers :( ")
			exit()
		if blood == None or ids[d[i][0]][3] in blood: 	
			print("\n", ids[d[i][0]], coord_to_name[d[i][1]], d[i][2])
			sucsex = ''
			while not sucsex:
				sucsex = input("Enter 'y' if request was fulfilled, or 'n' to continue: ")
				
	if sucsex[0]=="y" or sucsex[0]=="Y":
		print("\nCongrats!")


def call_nearest(addresses, target,  projectdirpath = "."):
	try:
		from records.algo import nearest
	except:
		from algo import nearest
	g = get_metro_coordinates_txt(projectdirpath)
	addlist = []
	for i in range( len(addresses) ):
		try:
			addlist.append(g[addresses[i]+" Metro Station"])
		except:
			pass
	from string import digits
	if target[0] not in digits:
		if " Metro Station" not in target:
			target = target+" Metro Station"
		if target not in g.keys():
			print("\nYour input was considered as the name of a metro station but it didn't match any. Please make sure that the name is exactly correct. It is recommended that you use latitude, longitude. ")
			exit()
		targ = g[target]

	else:
		targ = target.replace("° N", "")
		targ = targ.replace("° E", "")
		targ = targ.split(",")
		try:
			targ[0], targ[1] = float(targ[0]), float(targ[1])
		except:
			print("\nAn exception occured during parsing lat, long. Please make sure the format is correct.")
			exit()

	if(targ[0]<28.4 or targ[0]>28.9 or targ[1]<76.8 or targ[1]>77.4):
		print("\nNot in Delhi. Are you sure about the coordinates (lat, long)?")
		exit()

	return nearest(addlist, targ)

def get_metro_coordinates_txt(projectdirpath):
	f = open(projectdirpath+"/metro coordinates.txt")
	ff = f.read()
	f.close()
	from ast import literal_eval
	g = literal_eval(ff)
	return g

if __name__=="__main__":
	projectdirpath = input("Enter project directory or simply press Enter if it's in current directory: ") or '.'

	target = ''
	while not target:
		target = input("\nEnter exact metro station(eg. Vaishali) as it appears in 'metro coordinates.txt' or latitude, longitude(eg. 28.5681° N, 77.2058° E ) as returned by a google search(eg. on searching 'safdarjung hospital latitude longitude'): ").strip()
	blood = input("\nPlease enter space separated list of blood types you want(e.g. O+ B- A+) or simply press Enter if no preference: ").strip() or None
	if blood!=None:
		blood = blood.split()
	d, ids, coord_to_name = main(target, blood)
	showonterminalinterface(d, ids, coord_to_name)
