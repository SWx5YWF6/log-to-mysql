#!/usr/bin/python

# imports
import tailer
# https://pypi.org/project/tailer/
import mysql.connector
# https://pypi.org/project/mysql-connector-python/
# https://www.w3schools.com/python/python_mysql_insert.asp
from datetime import datetime
import telegram_send
from geolite2 import geolite2

# set database information
mydb = mysql.connector.connect(
  host="88.99.173.15",
  port="3306",
  user="username",
  password="password",
  database="log"
)

mycursor = mydb.cursor()

reader = geolite2.reader()

userUnknown = ": Failed password for invalid user"
userKnown = ": Failed password for"
SSHpublickey = "Accepted publickey for"

def SQLadd(datetime, user, ip, country):
  sql = "INSERT INTO ssh (time, username, srcIp, srcCountry, dstServer, dstCountry) VALUES (STR_TO_DATE(%(date)s,'%Y %b %d %k:%i:%s'), %(name)s, %(srcIpAddress)s, %(srcCountry)s, %(dstServer)s, %(dstCountry)s)"
  mycursor.execute(sql, { 'date': datetime, 'name': user, 'srcIpAddress': ip, 'srcCountry': country, 'dstServer': 'DE01', 'dstCountry': 'DE'})

  mydb.commit()
  #print(datetime, user, ip, country)

# Follow the file as it grows
for line in tailer.follow(open('/var/log/auth.log')):

  if userUnknown in line:
    list = line.split()
    currentYear = str(datetime.now().year)
    date = currentYear + " " + " ".join(list[0:3])
    user = list[10]

    ip = list[12]
    match = reader.get(ip)
    country = match['country']['iso_code']

    SQLadd(date, user, ip, country)

  elif userKnown in line:
    list = line.split()

    currentYear = str(datetime.now().year)
    date = currentYear + " " + " ".join(list[0:3])
    user = list[8]

    ip = list[10]
    match = reader.get(ip)
    country = match['country']['iso_code']

    SQLadd(date, user, ip, country)

  elif SSHpublickey in line:
    telegram_send.send(messages=[line], conf=None, disable_web_page_preview="true")
