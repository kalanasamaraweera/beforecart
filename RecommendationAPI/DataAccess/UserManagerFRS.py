#Manipualtes the CRUD Operations of Users in MySql

import MySQLdb as sql
import pymongo as m
from  neo4jrestclient.client import GraphDatabase
from py2neo import Graph ,authenticate 
from neo4jrestclient import client
import csv
import time
import datetime
import json

class UserManagerFRS(object):
    def __init__(self):
       UserManagerFRS =self
   
    def getNeo4jConfig(self):
       lines = [line.rstrip('\n') for line in open('NeoConf.txt')]
       elements =[]
       for element in lines:
           elements.append(element)
           
       return elements

    def createNewUserNode(self,userData):
      
       sts = self.checkUserExists(userData['email'])
       if sts == False:
           try: #user details
               username=userData['username']
               password =userData['password']
               email =userData['email']
               firstName =userData['firstname']
               lastName =userData['lastname']
               phone = userData['phone']
               address = userData['address']
               postal =userData['postal']
               state=userData['state']

               Id=self.getNewUserId()
       
       
               #Graph database config
               elements=[]
               elements =self.getNeo4jConfig()
               dbUrl = elements[0]
               dbUser = elements[1]
               dbPass = elements[2]


               db =GraphDatabase(dbUrl,dbUser,dbPass)
               user = db.labels.create("User")
               prop = db.nodes.create(userId=Id,username=username,password=password,email=email,firstName=firstName,lastName=lastName,phone=phone,state=state,address=address,postal=postal,cat1=0,cat2=0,cat3=0,cat4=0,cat5=0,cat6=0,cat7=0,cat8=0)
               user.add(prop)
               db.flush(True)

           except Exception:return False
           finally:return True
       else : return False
    
         


    def  getNewUserId(self):
       elements=[]
       elements =self.getNeo4jConfig()
       dbUrl = elements[0]
       dbUser = elements[1]
       dbPass = elements[2]


       db =GraphDatabase(dbUrl,dbUser,dbPass)
       query ="MATCH (`n: *`) RETURN count(*) as c"
       results =  db.query(query,returns = (str))
       for res in results:
           val= res[0]
       
       
       return int(val)+1
    

    def getUserId(self, email):

        query = "MATCH (n) WHERE n.email = '"+email+"' RETURN n.userId"
        elements=[] 
        elements = self.getNeo4jConfig()
        dbUrl = elements[0]
        dbUser= elements[1]
        dbPass=elements[2]
        graph = GraphDatabase(dbUrl,dbUser,dbPass)
        results= graph.query(query,returns = (int))

        cnt =0
        userId =0
        for res in results:
            cnt+=1
            
            userId = res[0]
        if cnt == 1:
            return userId
        else: return 0

    def checkUserExists(self,email):
        userId  =self.getUserId(email)
        if userId != 0:
            return True
        else :return False

        #Change property
    def updateProperty(self,userEmail,property,Val):
        upEmail=''
        try:
            userId =self.getUserId(userEmail)
            if userId != int(0) and property!="" and Val!="":
                query="MATCH(n {userId:"+str(userId)+"}) SET n."+str(property)+"='"+str(Val)+"' RETURN n.email"
                elements=[] 
                elements = self.getNeo4jConfig()
                dbUrl = elements[0]
                dbUser= elements[1]
                dbPass=elements[2]
                graph = GraphDatabase(dbUrl,dbUser,dbPass)
                results= graph.query(query,returns = (str))
           
                for result in results:
               
                    upEmail = result[0]

        except Exception,e:
            print str(e.message) 
            return False
        finally:
                Id=self.getUserId(upEmail)
                if userId == Id:
                    return True
                else: return False

                #Delete User Node
    def  removeUserNode(self,email):
        userId =0
        userId = self.getUserId(email)

        try:
           if userId != 0:
                elements = []
                elements = self.getNeo4jConfig()
                graph=Graph(elements[3])
                batch = graph.cypher.begin()     
                query = "MATCH(n:User) WHERE n.userId="+userId+" DELETE n"
                batch.append(query,{"userId":userId})
                batch.process()
                batch.commit()

           else: return False

                

        except  Exception,e:
            print e.message
            return False
        finally: return True 

       
        


        





       




