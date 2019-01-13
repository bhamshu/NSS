projectdirpath = input("Enter project directory or simply press Enter if it's in current directory: ") or '.'

csv_location = projectdirpath+'\\responses.csv'

def main(target, blood = None):
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


	f = open(projectdirpath+"\\metro coordinates.txt")
	f = f.read()
	exec("name_to_coord="+f, locals(), globals())
	coord_to_name = {v: k for k, v in name_to_coord.items()}

	d = call_nearest(addresses, target)
	
	f = open(projectdirpath+"\\dump.txt", "w")
	f.write(str(d))
	f.close()

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


def call_nearest(addresses, target):
	from algo import nearest
	f = open(projectdirpath+"\metro coordinates.txt")
	f = f.read()
	exec("g="+f, locals(), globals())
	
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

if __name__=="__main__":
	target = ''
	while not target:
		target = input("\nEnter exact metro station(eg. Vaishali) as it appears in 'metro coordinates.txt' or latitude, longitude(eg. 28.5681° N, 77.2058° E ) as returned by a google search(eg. on searching 'safdarjung hospital latitude longitude'): ").strip()
	blood = input("\nPlease enter space separated list of blood types you want(e.g. O+ B- A+) or simply press Enter if no preference: ").strip() or None
	if blood!=None:
		blood = blood.split()
	main(target, blood)
