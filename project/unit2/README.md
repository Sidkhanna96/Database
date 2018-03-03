Done by collaboration by Hee Soo Park and Sid Siddhant Khanna.

**Please Note Q1, Q2, Q3, Q4 is done in programming language C AND Q5, Q6 is done in programming language Python**

General: Please turn on the foreign key constraint in sqlite before executing/demo/testing these programs by typing in the terminal the following : 
“PRAGMA foreign_keys = ON;”


Q1: Choice of distance function: Our team have chosen “Haversine formula” to calculate the distance between two locations denoted by its latitude and longitude. Haversine is suitable for this question, because haversine formula determines the great-circle distance between two points on a sphere. Since we want to calculate the distance between two places on sphere (Earth) not a flat surface, Haversince formula is appropriate. The Haversine formula is a very accurate way of computing distance between two points on the surface of a sphere using the latitude and longitude of the two points. (Referenced:https://community.esri.com/groups/coordinate-reference-systems/blog/2017/10/05/haversine-formula)

Also I have referenced the subroutine for calculating the distance between two points referenced by latitude and longitude, from an online resource, which take latitude and longitude of the first node and latitude and longitude of the second node.
(Referenced:https://rosettacode.org/wiki/Haversine_formula#C)

Criteria: The distance must be computed by a new SQL function, called from a query in your code.
In your README.m file for this assignment, explain your choice of distance function. Your explanation will count for 1/2 mark towards your grade in this question.

To run the C program for Q1:
(1) download the appropriate database set, with correct table and attributes and constraints. (ex. “edmonton.db”).

(2) In the same directory as the database, compile C file with a gcc compiler by writing in terminal the following: “gcc -Wall -std=c99 q1.c -o q1 -lm -lsqlite3”

(3) Once q1.c file is compiled with a gcc compiler, an executable file named “q1” should have been created in the same directory.

(4) Now run the executable file, by typing in the order of executable file then database file and first nodeid and second noddid.
“./q1 databasefile(.db) first_node_id second_node_id”
(Ex. ./q1 edmonton.db 29770958 29811182)

(5) The executable program should be able to calculate the distance between two node_id referenced by latitude and longitude in format of Kilometres (KM).

Q2:
Assumptions: key and value are written in the format of “key=value” with out space inside the above quotations.
Each pair of key=value are separated by a space.

Criteria: The maximum distance must be computed by a SQL query that uses the function you created for Q1.


To run the C program for Q2:
(1) download the appropriate database set, with correct table and attributes and constraints. (ex. “edmonton.db”).

(2) In the same directory as the database, compile C file with a gcc compiler by writing in terminal the following: “gcc -Wall -std=c99 q2.c -o q2 -lm -lsqlite3”

(3) Once q2.c file is compiled with a gcc compiler, an executable file named “q2” should have been created in the same directory.

(4) Now run the executable file, by typing in the order of executable file then database file and desired number of “key=value” pairs.
“./q2 databasefile(.db) key_1=value_1 key_2=value_2 key_2=value_3
(Ex. ./q2 edmonton.db lit=yes maxspeed=100 highway=service)

(5) The executable program should be able to calculate the number of node elements from the desired pair of key=value, maximum distance of pairwise distance among those nodes in format of Kilometres (KM).

Q3:

Criteria: The length must be computed by a SQL query that uses the function you created for Q1.

To run the C program for Q4:

(1) download the appropriate database set, with correct table and attributes and constraints. (ex. “edmonton.db”).

(2) In the same directory as the database, compile C file with a gcc compiler by writing in terminal the following: “gcc -Wall -std=c99 q3.c -o q3 -lm -lsqlite3”

(3) Once q4.c file is compiled with a gcc compiler, an executable file named “q3” should have been created in the same directory.

(4) Now run the executable file, by typing in order of executable file database_file and way_id -> “./q3 edmonton.db wayid”
	eg ./q3 edmonton.db 4734665


Q4:
Assumptions: key and value are written in the format of “key=value” with out space inside the above quotations.

Each pair of key=value are separated by a space.

Criteria: All lengths must be computed in SQL, as in Q3.


To run the C program for Q4:
(1) download the appropriate database set, with correct table and attributes and constraints. (ex. “edmonton.db”).

(2) In the same directory as the database, compile C file with a gcc compiler by writing in terminal the following: “gcc -Wall -std=c99 q4.c -o q4 -lm -lsqlite3”

(3) Once q4.c file is compiled with a gcc compiler, an executable file named “q4” should have been created in the same directory.

(4) Now run the executable file, by typing in the order of executable file then database file and desired number of “key=value” pairs.
“./q4 databasefile(.db) key_1=value_1 key_2=value_2 key_2=value_3
(Ex. ./q4 edmonton.db lit=yes maxspeed=100 highway=service)

(5) The executable program should be able to calculate the number of way elements from the desired pair of key=value, and the length of the longest such path in format of Kilometres (KM).

Q5:

To run python program for Q5: (1) download the appropriate database set, with correct table and attributes and constraints. (ex. “edmonton.db”).

(2) In the same directory as the database, run the python program “q5.py” by the order in terminal of “python3 q5.py edmonton.db (way tsv filename).tsv”
ex. python3 q5.py edmonton.db way.tsv

Q6:

To run python program for Q6: (1) download the appropriate database set, with correct table and attributes and constraints. (ex. “edmonton.db”).


(2) In the same directory as the database, run the python program “q6.py” by the order in terminal of “python3 q6.py edmonton.db (node tsv file name).tsv”
