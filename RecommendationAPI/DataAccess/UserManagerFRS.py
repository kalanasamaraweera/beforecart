#Manipualtes the CRUD Operations of User Nodes in remote Neo4j repository

import MySQLdb as sql
import pymongo as m
from  neo4jrestclient.client import GraphDatabase
from py2neo import Graph ,authenticate 
from neo4jrestclient import client
import csv
import time
import datetime
import json
import logging
from DataAccess import DBConf


class UserManagerFRS(object):
    def __init__(self):
       UserManagerFRS =self
   
    #def getNeo4jConfig(self):

           


    def createNewUserNode(self,userData):
      
       sts = self.checkUserExists(userData['email'])
       Id=0
       if sts == False:
           try: #user details
               username=userData['username']
               password =userData['password']
               email =userData['email']
               firstName =userData['firstName']
               lastName =userData['lastName']
               phone = userData['phone']
               address = userData['address']
               postal =userData['postal']
               state=userData['state']

               Id=int(self.getNewUserId())
       
       
               #Graph database config
               elements=[]
               conf= DBConf.DBConf()
               elements =conf.getNeo4jConfig()
               dbUrl = elements[0]
               dbUser = elements[1]
               dbPass = elements[2]


               db =GraphDatabase(dbUrl,dbUser,dbPass)
               user = db.labels.create("User")
               prop = db.nodes.create(userId=str(Id),username=username,password=password,email=email,firstName=firstName,lastName=lastName,phone=phone,state=state,address=address,postal=postal,cat1=0,cat2=0,cat3=0,cat4=0,cat5=0,cat6=0,cat7=0,cat8=0)
               user.add(prop)
               db.flush(True)

           except Exception:return 0
           finally:return Id
       else : return -1
    
         


    def  getNewUserId(self):
       elements=[]
       conf= DBConf.DBConf()
       elements =conf.getNeo4jConfig()
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
        conf= DBConf.DBConf()
        elements =conf.getNeo4jConfig()        
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

    def getUserEmail(self,Id):

        Id =str(Id)
        elements=[] 
        conf= DBConf.DBConf()
        elements =conf.getNeo4jConfig()        
        dbUrl = elements[0]
        dbUser= elements[1]
        dbPass=elements[2]
        email=''
        try:
            graph = GraphDatabase(dbUrl,dbUser,dbPass)
            query = "MATCH (n) WHERE n.userId = '"+Id+"' RETURN n.email"
            results= graph.query(query,returns = (str))
            
            for res in results:
                email =res[0]
                break
        except Exception ,ex:
            print str(ex.message)
        finally:
            return email

        
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
                conf= DBConf.DBConf()
                elements =conf.getNeo4jConfig()
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
                conf= DBConf.DBConf()
                elements =conf.getNeo4jConfig()
                graph=Graph(elements[3])

                batch = graph.cypher.begin()     
                query = "MATCH(n:User) WHERE n.userId="+str(userId)+" DELETE n"
                batch.append(query,{"userId":userId})
                batch.process()
                batch.commit()
                

        except  Exception,e:
            print e.message
            return False

        finally: 
                if userId!=0: return True
                else: return False

    #remove all relationships of node
    def removeAllRels(self,email):
        userId =0
        userId = self.getUserId(email)

        try:

           if userId != 0:

                elements = []
                conf= DBConf.DBConf()
                elements =conf.getNeo4jConfig()
                graph=Graph(elements[3])

                batch = graph.cypher.begin()     
                query = "MATCH(n:User)-[r:FRIEND_OF]-(m:User) WHERE n.userId='"+str(userId)+"' DELETE r"
                batch.append(query,{"userId":userId})
                batch.process()
                batch.commit()
                

        except  Exception,e:
            print e.message
            return False

        finally: 
                if userId!=0: return True
                else: return False

    #return  list of the expertise levels of 8 product categories from locally
    def getCategoryExp(self,email):

        try:
            
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()
            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])

            query = "MATCH (n) Where  n.email='"+email+"'  return  n.cat1,n.cat2,n.cat3,n.cat4,n.cat5,n.cat6,n.cat7,n.cat8"
            results=  graphDatabase.query(query,returns = (str,str,str,str,str,str,str,str))
            for r in results:
                elements ={}
                elements ={1:r[0],2:r[1],3:r[2], 4:r[3],5:r[4],6:r[5],7:r[6],8:r[7]}
                return elements               
            

                
        except Exception ,e:
            print e.message
            return []

    #Return a set of matching users
    def searchUser(self,key,userId):
        try:
            
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()
            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])

            query = "MATCH (n) Where  n.email=~'"+key+".*' or n.firstName=~'"+key+".*' or n.lastName=~'"+key+".*'  return  n.userId,n.firstName,n.email"
            results=  graphDatabase.query(query,returns = (str,str,str))
            userDict =[]
            for r in results:
                elements ={}
                if userId != r[0]:
                    elements['userId']= r[0]
                    elements['firstName']=r[1]
                    elements['email'] =r[2]
                    userDict.append(elements)

                         
            
                
        except Exception ,e:
            print e.message
            return "{'userId':'0'}"
        finally:
            return userDict

    
    def getUserNode(self,email):

        try:
            
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()
            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])

            query = "MATCH (n) Where  n.email='"+email+"'  return  n.userId,n.firstName,n.email"
            results=  graphDatabase.query(query,returns = (str,str,str))
            for r in results:
                elements ={}
                elements['userId']= r[0]
                elements['firstName']=r[1]
                elements['email'] =r[2]
                if elements['email'] == email:
                    break               
                else:continue
                
        except Exception ,e:
            print e.message
            return '0'
        finally:return elements


    def validateUserData(self,data):
    
        username = data['username']
        if username == '':
            print  'empty username'
            return False
            

        password =  data['password']
        if password =='':
            print  'empty password'
            return False
        
        
        firstName = data['firstName']
        if firstName == '':
            print  'empty first name'
            return False


        lastName = data['lastName']
        if lastName =='':
            print ' empty last name'
            return False

   
        phone = str(data['phone'])
        if len(phone)!= 10:
            print ' invalid phone ;digits != 10'
            return False

                                 
        email = data['email']
        if email == '':
            print 'invalid email'
            return False

    
        address = data['address']
        if address == '':
             print 'empty address'
             return False
       

        state = data['state']
        if state == '':
            print 'empty state'
            return False
       

        postal = str(data['postal'])
        if len(postal) != 5:
            print 'empty postal'
            return False

        return True  
       

       
        


        





       




