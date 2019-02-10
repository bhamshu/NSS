def buildpage(d, ids, coord_to_name, blood, num = 10):
	ret = '''
	<style>
	table {
	  font-family: arial, sans-serif;
	  border-collapse: collapse;
	  width: 100%;
	}

	td, th {
	  border: 1px solid #dddddd;
	  text-align: left;
	  padding: 8px;
	}

	tr:nth-child(even) {
	  background-color: #dddddd;
	}
	</style>
	<table><tbody><tr><th>S.No</th><th>Name</th><th>Contact</th><th>Alt. Contact</th><th>Blood Group</th><th>Nearest Metro Station</th><th>Distance	</th></tr>''' #
	i = -1
	norecord = True
	shown = 0
	while True:
		i+=1
		if i>=len(d) or shown>=num:
			#print("\nSorry, out of volunteers :( ")
			break #exit()
		if blood == None or ids[d[i][0]][3] in blood: 
			shown+=1
			norecord = False
			ret+="<tr><td>" + str(shown)+"</td><td>"
			for k in ids[d[i][0]]:
				ret+=str(k)+"</td><td>"
			ret+=\
			str(coord_to_name[d[i][1]])+\
			"</td><td>"+str(d[i][2])+"</td>"#print("\n", ids[d[i][0]], coord_to_name[d[i][1]], d[i][2])
			#sucsex = "n"#sucsex = ''
			#while not sucsex:
			#	sucsex = input("Enter 'y' if request was fulfilled, or 'n' to continue: ")
	#if sucsex[0]=="y" or sucsex[0]=="Y":
	#	print("\nCongrats!")
	ret+='''</tbody></table>'''#
	if norecord:
		ret+='''<script>alert("Looks like there's no record with given blood groups. Sorry :(");</script>'''
	return ret #