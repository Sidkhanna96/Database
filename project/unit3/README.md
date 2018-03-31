CMPUT391
Project 3
Due March 3, 2018 midnight;

Team 29 (Sid Siddhant Khanna, Hee Soo Park)

**Please Note Q1, Q2, Q3, Q4, Q5 is done in programming language Python**

General: Please turn on the foreign key constraint in sqlite before executing/demo/testing these programs by typing in the terminal the following :
“PRAGMA foreign_keys = ON;”

* Download https://drive.google.com/file/d/1AfPoToovyq8rrsEisNOudhUPn0KNN5by/view and change directory to project directory containing the python files.

Q1:
  * Constant in the Q1 degree to meter calculator is based on the edmonton.db and would not calculate distance properly for larger distance files (confirmed with TA).

  Assumptions: database is correctly formatted

  Criteria: Print the SQL command to modify the database to STDOUT without modifying the database.

  To run the python program for Q1:
  (1) Open terminal
  (2) Change directory to the project folder containing q1.py and databasefile (i.e. edmonton.db).
  (3) In terminal run "cp edmonton.db unit3q1.db" (this will copy everything from edmonton.db to a new database (i.e. unit3q1.db)).
  (4) In terminal run "python3 q1.py edmonton.db > q1_output" (would run the program)
  (5) In terminal run "sqlite3 unit3q1.db < q1_output" (sqlite3 will run the database with all the queries inside q1_output)
  (6) In terminal run "sqlite3"
  (7) In sqlite3 run ".open unit3q1.db"
  (8) In sqlite3 run ".schema"
  (9) In sqlite3 run "SELECT * FROM nodeCartesian;"

Q2:
  To run the python program for Q2:
  (1) Open terminal
  (2) Change directory to project folder containing q2.py and dabasefile (i.e unit3q1.db).
  (3) In terminal run "cp unit3q1.db unit3q2.db"
  (4) In terminal run "python3 q2.py unit3q1.db > q2_output"
  (5) In terminal run "sqlite3 unit3q2.db < q2_output"
  (6) In terminal run "sqlite3"
  (7) In sqlite3 run ".open unit3q2.db"
  (8) In sqlite3 run ".schema"
  (9) In sqlite3 run "SELECT * FROM areaMBR"


Q3:
  * q3.md includes the SQlite commands and/or bash shell scripts to create both databases, starting from a legal database produced as specified for Unit 1.

  Criteria: Use SQlite's R-tree extensions, to create two SQLite database: unit3q3_btree.sql and unit3q3_rtree.sql

  To create two SQLite databases: unit3q3_btree.sql and unit3q3_rtree.sql.
  (1) Open terminal
  (2) Change directory to project folder containing q3.md and previous project files.
  (3) cp unit3q2.db unit3q3_btree.db (creating the btree database : this is just copying everything from the second question database to another database called the unit3_btree database)
  (4) In terminal run "sqlite3 unit3q3_btree.db"
  (5) In sqlite3 execute the first paragraph of queries in q3.md
  (4) cp unit3q2.db unit3q3_rtree.db (creating the rtree database : this is just copying everything from the second question database to another database called the unit3_rtree database)
  (6) In sqlite3 run ".q"
  (7) In terminal run "sqlite3 unit3q3_rtree.db"
  (8) In sqlite3 execute the second paragraph of queries in q3.md


Q4:
  * q4.md includes the table with the results of the program for k=100, the following values of 1={25,50,75,100,125} and for the two databases unit3q3_btree.db and unit3q3_rtree.db

  Criteria: Computes the average time, out of k runs, to execute a SQL query to find the number of areas from areaMBR that are contained in a randomly gernerated bounding rectangles.

  To run the python program for Q4:
  (1) Open terminal
  (2) Change directory to project folder containing q4.py and dabasefile.
  * skeleton of q4: "python3 q4.py (btree/rtree) I K"
  (3) In terminal run "python3 q4.py unit3q3_btree.db L K"
  (ex.) "python3 q4.py unit3q3_btree.db 25 100"
  (4) In terminal run "python3 q4.py unitq3q_rtree.db L K"
  (ex.) "python3 q4.py unit3q3_rtree.db 25 100"

  * execution of rtree is usually faster and bteer than btree

Q5:
  Criteria: find the K areas (in areaBMR) that are closest to query point (x,y).
            Print to STDOUT the ids of these areas and their distance to query point, sorted by increasing distance.

  To run the python program for Q5:
  (1) Open terminal
  (2) Change directory to project folder containing q5.py and databasefile.
  (3) In terminal run "python3 q5.py unit3q3_rtree.db x(coordinate) y(coordinate) k(k nearest areas)"
  (ex.) "python3 q5.py unit3q3_rtree.db 20 50 20"
