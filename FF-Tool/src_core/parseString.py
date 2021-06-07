import argparse

#def devideIntoKeyAndValue(str) #input: just string, unparsed; 

def isNotFloat(elem):
	try:
		float(elem)
		return False
	except ValueError:
		return True

def stringIsInt(elem):
	if not type(elem) is str: raise ValueError
	try:
		int(elem)
		return True
	except ValueError:
		return False

def isKey(elem):
	return isNotFloat(elem) or stringIsInt(elem)


def getKeysAddValues(l):
	l = l.replace(';',' ').split() #now it's a list of elements
	#print l
	keys = []
	values = []

	######## FOR:
	for j in range(len(l)):
		if isKey(l[j]):
			keys.append(l[j])
		else:
		#elif not isNotFloat(l[j]):
			values.append(float(l[j]))

	#print "Keys  : %s" %keys
	#print "Values: %s" %values
	return (keys, values)