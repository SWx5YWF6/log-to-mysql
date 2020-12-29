#!/usr/bin/python

# imports
import tailer
# https://pypi.org/project/tailer/
import mysql.connector
# https://pypi.org/project/mysql-connector-python/
# https://www.w3schools.com/python/python_mysql_insert.asp
from datetime import datetime

# set database information
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
