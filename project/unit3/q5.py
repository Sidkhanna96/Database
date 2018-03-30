import sys
import sqlite3
import math

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()


def MINDIST(id, x, y, minX, maxX, minY, maxY):
	# print(id, x, y, minX, maxX, minY, maxY)
	Px = float(x)
	Py = float(y)
	Sx = float(minX)
	Sy = float(minY)
	Tx = float(maxX)
	Ty = float(maxY)

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
		mindist.append(MINDIST(elem[0],x, y, elem[1],elem[2],elem[3],elem[4]))

	return mindist


def objectDist(id, x, y, minX, minY, maxX, maxY):
	midX = (maxX - minX) /2
	midY = (maxY - minY) /2

	distP = (x**2 + y**2)
	distMid = (midX**2 + midY**2)

	actualDist = (distP + distMid)**1/2
	return actualDist

def MinMaxDist(id, x, y, minX, maxX, minY, maxY):
	Px = x
	Py = y
	Sx = minX
	Sy = maxX
	Tx = minY
	Ty = maxY

	xValue = 0
	yValue = 0

	if(Px <= (Sx + Tx)/2):
		Rmx = Sx
	else:
		Rmx = Tx

	if(Py <= (Sy + Ty)/2):
		Rmy = Sy
	else:
		Rmy = Ty


	if(Px >= (Sx + Tx)/2):
		rMx = Sx
	else:
		rMx = Tx

	if(Py >= (Sy + Ty)/2):
		rMy = Sy
	else:
		rMy = Ty
	
		

	min(xValue, yValue)


def pruneDownBranchList(Node, x, y, Nearest, branchList):
	values = []
	mindist = []

	cursor.execute("""SELECT rtreenode(2, data) from areaMBR_node WHERE nodeno == ?""", (Node,))
	result = cursor.fetchall()
	
	result = result[0][0].split("} {")
	for elem in result:
		elem = elem.replace("{", "")
		elem = elem.replace("}", "")
		values.append(elem.split(" "))
	print(values)
	for elem in values:
		MinMaxDist(int(elem[0]), int(x), int(y), int(elem[1]), int(elem[2]), int(elem[3]), int(elem[4]))


def nearestNeighBours(Node, x, y, Nearest):
	newNode = 0
	branchList = []
	dist = 0
	last = 0
	i = 0 
	# rectangle = 0
# 
	cursor.execute("SELECT count(*) FROM areaMBR_parent ap WHERE ap.parentnode == ?", (Node,))
	isLeaf = cursor.fetchall()
	
	if(isLeaf[0][0] == 0):
		cursor.execute("SELECT * FROM areaMBR WHERE rowid IN (SELECT rowid FROM areaMBR_rowid WHERE nodeno == ?)", (Node,))
		result = cursor.fetchall()
		# print(result)
		for elem in result:
			id = int(elem[0])
			minX = int(elem[1])
			maxX = int(elem[2])
			minY = int(elem[3])
			maxY = int(elem[4])
			dist = objectDist(id, int(x), int(y), minX, maxX, minY, maxY)
			# print(dist)
			if(dist < Nearest):
				Nearest = dist
				rectangle = id

	else:
		# Generate Active Branch List
		branchList = genBranchList(x, y, Node, branchList)

		#sorting
		branchList.sort(key=lambda dist:dist[1])

		#Downward Pruning
		last = pruneDownBranchList(Node, x, y, Nearest, branchList)
		# print(last)
		# last = branchList

		# for i in range(0, len(last)):
		# 	newNode = branchList[i][0]

			# nearestNeighBours(newNode, x, y, Nearest)


if __name__ == '__main__':
	x = sys.argv[2]
	y = sys.argv[3]
	k = sys.argv[4]

	cursor.execute("SELECT DISTINCT an.nodeno FROM areaMBR_node an WHERE an.nodeno NOT IN (SELECT nodeno FROM areaMBR_parent);")
	Node = cursor.fetchall()

	nearestNeighBours(Node[0][0], x, y, math.inf)