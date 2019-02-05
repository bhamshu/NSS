from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def nearest(arr, astr):
	ret = [0, None]
	for i in arr:
		d = similar(i, astr)
		if(d>ret[0]):
			ret[0] = d
			ret[1] = i
	if(ret[0]>0):
		return ret[1]


f = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\metro stations form.txt")
a = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\metro stations api.txt")

f = f.read()
a = a.read()

exec("f = "+f)
exec("a = "+a)

dic = {}

for i in f: 
	if i not in a:
		c = nearest(a, i)
		dic[i] = c
f = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\map_f_to_a.txt", "w")
f.write(str(dic))
f.close()
#check manually
#exceptions: haiderpur
#harkesh nagar okhla
#
#