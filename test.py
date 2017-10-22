import MySQLdb
db = MySQLdb.connect("localhost", "root", "asdf123", "serviceMyWheels" )
cursor = db.cursor()
sql = "select *from core_crewmember"
cursor.execute(sql)
results = cursor.fetchall()
arr = [];
map = {}
str="anil"
for i in range(len(str)):
    arr.append(i)

map["a"] = arr
map["b"] ="anil"
print map

# for row in results:
#       name = row[4]
#       address = row[5]
#       print name
#       print address

db.close()