# Project 1 README:
(1) extract border of Edmonton from Map of Alberta by writing following in the command line within /osmosis/bin
./osmosis --read-pbf /cshome/skhanna1/Desktop/391/alberta-latest.osm.pbf --bounding-box bottom=53.3841 left=-113.7373 right=-113.2361 top=53.7203 --write-xml edmonton.osm

(2) Run python proram to parase,
  python3 main.py
  
(3) open sqlite3 from command line.
  by typing "sqlite3" in command line.
  
(4) in command line ".open databse.db"
  then ".read triggers.sql" in command line with sqlite3 running.



