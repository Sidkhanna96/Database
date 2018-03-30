import sys
import sqlite3


def convertLat(minlat, lat):
	difference = lat - minlat
	meterlat = difference*111286
	return meterlat 

def convertLon(minlon, lon):
	difference = lon - minlon
	meterlon = difference*67137
	return meterlon 

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

if __name__ == '__main__':

	print("""DROP TABLE IF EXISTS nodeCartesian;""")
	# cursor.execute("""CREATE TABLE nodeCartesian(id int, x FLOAT, y FLOAT, PRIMARY KEY(id));""")
	print("CREATE TABLE nodeCartesian(id int, x FLOAT, y FLOAT, PRIMARY KEY(id));")
	
	cursor.execute("""SELECT id, min(lat), min(lon) FROM node;""")
	result = cursor.fetchone()
	# print(result)
	minlat = result[1]
	minlon = result[2]

	cursor.execute("""SELECT * FROM node;""")
	result2 = cursor.fetchall()
	
	k = 0

	print("""INSERT INTO nodeCartesian(id, x, y) VALUES """)
	for r in result2:
		meterlat = convertLat(minlat, r[1])
		meterlon = convertLon(minlon, r[2])
		if(k < len(result2) - 1):
			print("(", r[0], ",", meterlon, ",", meterlat, ")", ",", end="")
			k = k + 1
		else:
			print("(", r[0], ",", meterlon, ",", meterlat, ")", ";", end="")

	connection.commit()