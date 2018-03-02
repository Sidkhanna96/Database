import sys
import csv
import sqlite3

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

if __name__ == '__main__':
  # print(sys.argv[2])
  with open(sys.argv[2]) as fd:
    rd = csv.reader(fd, delimiter="\t")
    for row in rd:
      cursor.execute("""INSERT INTO node VALUES(:id, :lt, :ln)""",{'id':row[0], 'lt':row[1], 'ln':row[2]})
      if(len(row)>3):
        for elem in range(len(row)):
          if(elem>2):
            # print(row[0])
            # print(row[elem].split("=")[0])
            # print(row[elem].split("=")[1])
            cursor.execute("""INSERT INTO nodetag VALUES(:nid, :k, :v)""",{'nid':row[0],'k':row[elem].split("=")[0],'v':row[elem].split("=")[1]})
        # print("~~~~~~~~`")
  connection.commit()