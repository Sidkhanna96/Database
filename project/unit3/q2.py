# SELECT wp.wayid, min(n.lat), max(n.lat), min(n.lon), max(n.lon)
# FROM way w, waypoint wp, node n
# WHERE w.id == wp.wayid
# AND wp.nodeid == n.id
# AND w.closed == 1
# GROUP BY wp.wayid;

# 322236325|53.4764316|53.4765018|-113.3945867|-113.3943369


import sys
import sqlite3

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

if __name__ == '__main__':
	print("""DROP TABLE IF EXISTS areaMBR;""")
	# cursor.execute("""CREATE TABLE areaMBR(id, minX, maxX, minY, maxY, PRIMARY KEY(id));""")
	print("CREATE TABLE areaMBR(id, minX, maxX, minY, maxY, PRIMARY KEY(id));")

	cursor.execute("""SELECT wp.wayid, min(nc.x), max(nc.x), min(nc.y), max(nc.y)
						FROM nodeCartesian nc, way w, waypoint wp
						WHERE w.id == wp.wayid
						AND wp.nodeid == nc.id
						AND w.closed == 1
						GROUP BY wp.wayid;""")
	result = cursor.fetchall()

	k = 0

	print("""INSERT INTO areaMBR(id, minX, maxX, minY, maxY) VALUES """)
	for r in result:
		if(k < len(result) - 1):
			print("(", r[0], "," ,r[1], ",", r[2], ",", r[3], "," ,r[4] , ")", ",", end="")
			k = k + 1
		else:
			print("(", r[0], "," ,r[1], ",", r[2], ",", r[3], "," ,r[4] , ")", ";", end="")

	connection.commit()