#!/usr/bin/python

import MySQLdb as sql

#Create MYSQL database connection
class MySqlConnection(object):
    
    connection 

    def __init__ (self):
      MySqlConnection= self
      

    def cancelConnection(self):
        self.connection.close()
    
    def makeConnection(self,query):
        #open connection
       connection =sql.connect("localhost","root","","beforecart") #localhost-url with port; root -username- ""-password beforecart-database_name
       
       #prepare a cursor object using cusor() method
       cursor = connection.cursor()

       #execute SQL query using execute() methods
       
       cursor.execute(query)
       
       #Fetch Result to variable
       data = cursor.fetchone()

       print "Database version %s"% data





      



