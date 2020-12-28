#!/usr/bin/python

# imports
import tailer
import mysql.connector
# https://www.w3schools.com/python/python_mysql_insert.asp

# set database information
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()

# Follow the file as it grows
for line in tailer.follow(open('/var/log/syslog')):
    # check if is SSH login
    for unwantedUrl in blocklist:
        # if there exist a line with a entry on the blocklist, do 'telegram-send'
        if unwantedUrl in line:
            # disabling potential links to be clickable by putting the dot between brackets
            safeUrl = line.replace(".", "[.]")
            telegram_send.send(messages=[safeUrl], conf=None, disable_web_page_preview="true")
