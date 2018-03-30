import sys
import sqlite3
import random
import time

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

if __name__ == '__main__':

	l = int(sys.argv[2])
	k = int(sys.argv[3])
	total_time = 0

	rectangle_width = random.uniform(1, 10) * l
	rectangle_height = random.uniform(1, 10) * l

	rectangle_area = rectangle_width*rectangle_height

	cursor.execute("""SELECT min(minX), max(maxX), min(minY), max(maxY) FROM areaMBR;""")
	result = cursor.fetchall()
	j = k

	while(k):
		i = 1
		while(i == 1):
			x_low_l = random.uniform(result[0][0], result[0][1]) 
			y_low_l = random.uniform(result[0][2], result[0][3])
		
			y_up_l = y_low_l + rectangle_height
			x_low_r = x_low_l + rectangle_width
			# Rectangle does not exceed boundary 
			if(y_up_l <= result[0][3] and x_low_r <= result[0][1]):
				#check if has atleast 1 MBR in random rectangle
				cursor.execute("""SELECT COUNT(*) 
									FROM areaMBR a 
									WHERE a.minX BETWEEN ? AND ? 
									AND a.minX BETWEEN ? AND ?
									OR a.maxX BETWEEN ? AND ?
									AND a.maxX BETWEEN ? AND ?
									OR a.minY BETWEEN ? AND ?
									AND a.minY BETWEEN ? AND ?
									OR a.maxY BETWEEN ? AND ?
									AND a.maxY BETWEEN ? AND ?;""",(x_low_l, x_low_r, y_low_l, y_up_l, x_low_l, x_low_r, y_low_l, y_up_l, x_low_l, x_low_r, y_low_l, x_low_l, x_low_r, y_up_l, y_low_l, y_up_l))
				result2 = cursor.fetchall()
				if result2[0][0] > 0:
					i = 0

		cursor.execute("""DROP TABLE IF EXISTS rectangle_random;""")
		cursor.execute("""CREATE TABLE rectangle_random(minX, maxX, minY, maxY);""")
		cursor.execute("""INSERT INTO rectangle_random VALUES(?,?,?,?);""",(x_low_l, x_low_r, y_low_l, y_up_l))

		#Finding the number of rectangles (completely) inside the random rectangle
		start_time = time.time()
		# if "btree" in sys.argv[1]:
		cursor.execute("""SELECT COUNT(*) 
							FROM areaMBR a 
							WHERE a.minX BETWEEN ? AND ? 
							AND a.maxX BETWEEN ? AND ?
							AND a.minY BETWEEN ? AND ?
							AND a.maxY BETWEEN ? AND ?;""",(x_low_l, x_low_r, x_low_l, x_low_r, y_low_l, y_up_l, y_low_l, y_up_l))
		# else:
		# 	cursor.execute("""SELECT COUNT(*) 
		# 					FROM area_common a 
		# 					WHERE a.minX BETWEEN ? AND ? 
		# 					AND a.maxX BETWEEN ? AND ?
		# 					AND a.minY BETWEEN ? AND ?
		# 					AND a.maxY BETWEEN ? AND ?;""",(x_low_l, x_low_r, x_low_l, x_low_r, y_low_l, y_up_l, y_low_l, y_up_l))

		result3 = cursor.fetchall()
		# print(result3[0][0], j)
		if(int(result3[0][0])!=0):
			print(result3[0][0], k)
			total_time = total_time + (time.time() - start_time)
			k = k - 1
		# print(time.time() - start_time)

	average_time = total_time/j
	print(j, "\t", l, "\t", average_time)
	connection.commit()