#!/usr/bin/python

import MySQLdb as sql

#Create MYSQL database connection
class MySqlConnection(object):
    
    connection 

    def __init__ (self):
      MySqlConnection= self
      

    def cancelConnection(self):
        self.connection.close()
    
    def makeConnection(self):
        #open connection
       connection =sql.connect("localhost","root","","beforecart")
       
       #prepare a cursor object using cusor() method
       cursor = connection.cursor()

       #execute SQL query using execute() methods
       query ="select VERSION()"
       cursor.execcute(query)
       
       #Fetch Result to variable
       data = cursor.fetchone()

       print "Database version %s"% data





      



