#!/usr/bin/python

# imports
#  https://pypi.org/project/tailer/
import tailer
#  https://pypi.org/project/mysql-connector-python/
import mysql.connector
from datetime import datetime

# set database information
#  https://www.w3schools.com/python/python_mysql_insert.asp
#  the database and tables have to be created before running this script. below the 'CREATE TABLE' statement I used in this case:

#CREATE TABLE ssh_attempt.log (
#  id INT AUTO_INCREMENT,
#  time DATETIME NOT NULL,
#  username VARCHAR(100),
#  srcIp VARCHAR(15),
#  PRIMARY KEY(id)
#);

#  make sure your user has the correct permissions on the database.
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)
mycursor = mydb.cursor()

userUnknown = ": Failed password for invalid user"
userKnown = ": Failed password for"
currentYear = str(datetime.now().year)

def SQLadd(datetime, user, ip):
  sql = "INSERT INTO log (time, username, srcIp) VALUES (STR_TO_DATE(%(date)s,'%Y %b %d %k:%i:%s'), %(name)s, %(ipAddress)s)"
  mycursor.execute(sql, { 'date': datetime, 'name': user, 'ipAddress': ip })

  mydb.commit()
  print(datetime, user, ip)

# Follow the file as it grows
for line in tailer.follow(open('/var/log/auth.log')):
  #
  if userUnknown in line:
    list = line.split()
    date = currentYear + " " + " ".join(list[0:3])
    user = list[10]
    ip = list[12]
    SQLadd(date, user, ip)
  elif userKnown in line:
    list = line.split()
    date = currentYear + " " + " ".join(list[0:3])
    user = list[8]
    ip = list[10]
    SQLadd(date, user, ip)
