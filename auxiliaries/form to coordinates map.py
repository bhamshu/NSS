c = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\metro coordinates.txt").read()
f = open(r"C:\Users\Orwell\Desktop\irrelevant\College\Computing\blood donation project\metro stations form.txt").read()


exec("c = "+c);
exec("f = "+f);
c = list(c.keys())

for i in f:
	if i+" Metro Station" not in c:
		print(i)

print("111")
for i in c:
	if not i.endswith(" Metro Station"):
		print(i)


