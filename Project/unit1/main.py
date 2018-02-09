#import necessary library that exists in lab machine.
#Hee Soo Park
#Sid Siddhant Khanna

import sqlite3
import xml.etree.ElementTree as ET
import time

start_time = time.time()

x = input("Enter name of database you wish to create: ")
y = input("Enter inputfile name: ")

connection = sqlite3.connect(x)
cursor = connection.cursor()
inputfile = y
tree = ET.parse(y)
root = tree.getroot()

#drop all the tables that I will create, for repetitive run.
def droptable():
    cursor.execute("DROP TABLE IF EXISTS node;")
    cursor.execute("DROP TABLE IF EXISTS way;")
    cursor.execute("DROP TABLE IF EXISTS waypoint;")
    cursor.execute("DROP TABLE IF EXISTS nodetag;")
    cursor.execute("DROP TABLE IF EXISTS waytag;")
    connection.commit()

#create all the tables needed and commit
def createtable():
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("CREATE TABLE node (id integer, lat float, lon float, PRIMARY KEY(id));")
    cursor.execute("CREATE TABLE way (id integer, closed boolean, PRIMARY KEY(id));")
    cursor.execute("""CREATE TABLE waypoint (wayid integer, ordinal integer, nodeid integer,CONSTRAINT fk_wayid
        FOREIGN KEY (wayid) REFERENCES way(id) ON DELETE CASCADE, CONSTRAINT fk_nodeid FOREIGN KEY (nodeid) REFERENCES node(id) ON DELETE CASCADE);""")
    cursor.execute("CREATE TABLE nodetag (id integer, k text, v text, CONSTRAINT fk_nodetag FOREIGN KEY(id) REFERENCES node(id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE waytag (id integer, k text, v text, CONSTRAINT fk_waytag FOREIGN KEY(id) REFERENCES way(id) ON DELETE CASCADE);")
    connection.commit()

#insert node with correct constraints and parameters
def insertnode(nodeid, lat, lon):
    cursor.execute('''INSERT INTO node VALUES (:nodeid, :lat, :lon);''',{'nodeid':nodeid, 'lat':lat, 'lon':lon})

#insert way with correct constraints and parameters
def insertway(wayid, closed):
    cursor.execute('''INSERT INTO way VALUES (:wayid, :closed);''',{'wayid':wayid, 'closed':closed})

#insert waypoint with correct constraints and parameters
def insertwaypoint(wayid, ordinal, nodeid):
    cursor.execute('''INSERT INTO waypoint VALUES (:wayid, :ordinal, :nodeid);''',{'wayid':wayid, 'ordinal':ordinal, 'nodeid':nodeid})

#insert nodetag with correct constraints and parameters
def insertnodetag(node_id, k, v):
    cursor.execute('''INSERT INTO nodetag VALUES (:id, :k, :v);''',{'id':node_id, 'k':k, 'v':v})

#insert waytag with correct constraints and parameters
def insertwaytag(way_id, k, v):
    cursor.execute('''INSERT INTO waytag VALUES (:id, :k, :v);''',{'id':way_id, 'k':k, 'v':v})

#Start parsing nodes
def node():
    print("STARTING")
    #create a list to append the nodes within way to check for closed
    closedlist = []
    closed = False
    node_id = 0
    way_id = 0
    #parsing throught nodes and inserting
    for elem in root.iter():
        if(elem.tag == 'node'):
            node_id = elem.get('id')
            node_lat = elem.get('lat')
            node_lon = elem.get('lon')
            insertnode(node_id, node_lat, node_lon)
            for node_elements in elem:
                if(node_elements.tag == 'tag'):
                    k = node_elements.get('k')
                    v = node_elements.get('v')
                    insertnodetag(node_id, k, v)
    connection.commit()


def way():
    closedlist = []
    closed = False
    node_id = 0
    way_id = 0
    for elem in root.iter():
        if(elem.tag == 'way'):
            way_id = elem.get('id')
            #parsing through way and inserting
            for way_elements in elem:
                if(way_elements.tag == 'nd'):
                    closedlist.append(way_elements.get('ref'))

            if(len(closedlist)>0):
                #if closed list is not empty, then if the first element is equal to last element of the list, then it is a closed lit.
                if(closedlist[0] == closedlist[len(closedlist)-1]):
                    closed = True
                else:
                    closed = False
            #determine closed or open and insert into way.
            insertway(way_id, closed)

            #parsing through way_tag and inserting.
            for way_elements in elem:
                if(way_elements.tag == 'tag'):
                    k = way_elements.get('k')
                    v = way_elements.get('v')
                    insertwaytag(way_id, k, v)

            for x in closedlist:
                try:
                    #inserting way point
                    insertwaypoint(way_id, closedlist.index(x), x)
                except:
                    pass
        #reset closed list for next way.
        closedlist = []
    connection.commit()


if __name__ == '__main__':
    droptable()
    createtable()
    node()

    print("Time = ", time.time() - start_time)

    way()
