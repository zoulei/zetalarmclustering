import os
def removedup():
	f = open("../itemmining")
	of = open("../tmp","w")
	for line in f:
		itemlist = line.strip().split(" ")
		itemlist = list(set(itemlist))
		itemstr = " ".join(itemlist) + "\n"
		of.write(itemstr)
	f.close()
	of.close()
	os.system("cp ../tmp ../itemmining")