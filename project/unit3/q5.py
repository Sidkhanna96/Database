import sys
import sqlite3
import math

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()


def MINDIST(id, x, y, minX, maxX, minY, maxY):
	# print(id, x, y, minX, maxX, minY, maxY)
	id = id
	Px = x
	Py = y
	Sx = minX
	Sy = minY
	Tx = maxX
	Ty = maxY

	if(Px < Sx):
		Rx = Sx
	elif(Px > Tx):
		Rx = Tx
	else:
		Rx = Px
	if(Py < Sy):
		Ry = Sy
	elif(Py > Ty):
		Ry = Ty
	else:
		Ry = Py
	

	mindistX = abs(Px - Rx)**2
	mindistY = abs(Py - Ry)**2
	mindist = mindistX + mindistY

	return id, mindist

def genBranchList(x, y, Node, branchList):
	values = []
	mindist = []

	cursor.execute("""SELECT rtreenode(2, data) from areaMBR_node WHERE nodeno == ?""", (Node,))
	result = cursor.fetchall()
	
	result = result[0][0].split("} {")
	for elem in result:
		elem = elem.replace("{", "")
		elem = elem.replace("}", "")
		values.append(elem.split(" "))

	for elem in values:
		mindist.append(MINDIST(float(elem[0]),float(x), float(y), float(elem[1]),float(elem[2]),float(elem[3]),float(elem[4])))

	return mindist


def objectDist(id, x, y, minX, maxX, minY, maxY):
	midX = (maxX - minX) /2 + minX
	midY = (maxY - minY) /2 + minY

	distY = abs(midY - y)**2
	distX = abs(x- midX)**2

	actualDist = math.sqrt(distY + distX)

	# distP 

	# distP = (x**2 + y**2)
	# distMid = (midX**2 + midY**2)

	# actualDist = (distP + distMid)**1/2
	return id, actualDist

def MinMaxDist(id, x, y, minX, maxX, minY, maxY):
	Px = x
	Py = y
	Sx = minX
	Sy = maxX
	Tx = minY
	Ty = maxY

	if(Px <= (Sx + Tx)/2):
		rmx = Sx
	else:
		rmx = Tx

	if(Py <= (Sy + Ty)/2):
		rmy = Sy
	else:
		rmy = Ty


	if(Px >= (Sx + Tx)/2):
		rMx = Sx
	else:
		rMx = Tx

	if(Py >= (Sy + Ty)/2):
		rMy = Sy
	else:
		rMy = Ty
	

	valX = math.pow(abs(Px - rmx), 2) + math.pow(abs(Py - rMy),2)
	valY = math.pow(abs(Py - rmy),2) + math.pow(abs(Px - rMx), 2)
		

	minmaxdist = min(valX, valY)
	return id, minmaxdist

def pruneBranchList(Node, x, y, Nearest, branchList):
	values = []
	mindist = []
	mmBranchList = []

	cursor.execute("""SELECT rtreenode(2, data) from areaMBR_node WHERE nodeno == ?""", (Node,))
	result = cursor.fetchall()
	
	result = result[0][0].split("} {")
	for elem in result:
		elem = elem.replace("{", "")
		elem = elem.replace("}", "")
		values.append(elem.split(" "))
	for elem in values:
		mmDist = MinMaxDist(float(elem[0]), float(x), float(y), float(elem[1]), float(elem[2]), float(elem[3]), float(elem[4]))
		mmBranchList.append(mmDist)

	copybranch = branchList

	for mmDist in mmBranchList:
		for Dist in branchList:
			if(mmDist[0] != Dist[0]):
				if(Dist[1] > mmDist[1]):
					branchList.remove(Dist)

	return branchList




def nearestNeighBours(Node, x, y, Nearest):
	newNode = 0
	branchList = []
	dist = 0
	last = 0
	i = 0 

	cursor.execute("SELECT count(*) FROM areaMBR_parent ap WHERE ap.parentnode == ?", (Node,))
	isLeaf = cursor.fetchall()
	
	if(isLeaf[0][0] == 0):
		cursor.execute("SELECT rtreenode(2, data) from areaMBR_node WHERE nodeno == ?", (Node,))
		result = cursor.fetchall()
		values = []
		result = result[0][0].split("} {")
		for elem in result:
			elem = elem.replace("{", "")
			elem = elem.replace("}", "")
			values.append(elem.split(" "))
		
		for elem in values:
			# print(elem)
			id = float(elem[0])
			minX = float(elem[1])
			maxX = float(elem[2])
			minY = float(elem[3])
			maxY = float(elem[4])
			dist = objectDist(id, float(x), float(y), float(minX), float(maxX), float(minY), float(maxY))
			Nearest.append(dist)

	else:
		# Generate Active Branch List
		branchList = genBranchList(x, y, Node, branchList)

		#sorting
		branchList.sort(key=lambda dist:dist[1])

		#Downward Pruning
		last = pruneBranchList(Node, x, y, Nearest, branchList)

		for i in range(0, len(last)):
			newNode = last[i][0]

			Nearest = nearestNeighBours(newNode, x, y, Nearest)

	return Nearest

if __name__ == '__main__':
	x = sys.argv[2]
	y = sys.argv[3]
	k = sys.argv[4]

	cursor.execute("SELECT DISTINCT an.nodeno FROM areaMBR_node an WHERE an.nodeno NOT IN (SELECT nodeno FROM areaMBR_parent);")
	Node = cursor.fetchall()

	value = nearestNeighBours(Node[0][0], x, y, [])
	value.sort(key = lambda dist: dist[1])
	value = value[0:int(k)]
	# print(value)
	for elem in value:
		print("id: ", elem[0], "\tDistance: ", elem[1])