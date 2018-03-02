import sys
import csv
import sqlite3

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

if __name__ == '__main__':
  with open(sys.argv[2]) as fd:
    rd = csv.reader(fd, delimiter="\t")
    num = 0
    list_k = []
    list_v = []
    for row in rd:
    	if(num%3==0):
    		wayid = row[0]
    		for elem in row:
    			if("=" in elem):
    				list_k.append(elem.split("=")[0])
    				list_v.append(elem.split("=")[1])
    		if(len(list_k) > 0):
    			for i in range(len(list_k)):
    				# print(list_k[i], list_v[i])
	    			cursor.execute("""INSERT INTO waytag VALUES(:wayid, :k, :v)""",{'wayid':wayid, 'k':list_k[i], 'v':list_v[i]})
	    			pass
    		list_k = []
    		list_v = []

    	if(num%3==1):
    		# print(row)
    		for i in range(len(row)):
    			pass
    			# print(wayid, i, row[i])
    			cursor.execute("""INSERT INTO waypoint VALUES(:wayid, :ordinal, :nodeid)""", {'wayid':wayid, 'ordinal':i, 'nodeid':row[i]})
    		if(row[0] == row[len(row)-1]):
    			closed = 1
    			# print(wayid, closed)
    			cursor.execute("""INSERT INTO way VALUES(:wayid, :closed)""",{'wayid':wayid, 'closed':closed})
    		else:
    			closed = 0
    			# print(wayid, closed)
    			cursor.execute("""INSERT INTO way VALUES(:wayid, :closed)""",{'wayid':wayid, 'closed':closed})

    	if(num%3==2):
    		pass
    	num += 1

    connection.commit()
