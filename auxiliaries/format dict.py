f = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\dict.txt")
d = f.read()
d = d.split("\n")
dic = {}
for i in d:
	j = i.index("<td class='left'><a href='/")+27
	k = i.index("station'>")+7
	l = i.index('</a>')
	dic[i[k+2:l]] = i[j:k]

f = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\_dict.txt", "w")
f.write(str(dic))
f.close()


