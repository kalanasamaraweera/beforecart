from  neo4jrestclient.client import GraphDatabase
from DataAccess import UserManagerFRS
from py2neo import Graph ,authenticate 
from neo4jrestclient import client
import csv
import time
import datetime
import json

#FriendshipBuilderFRS class implements CRUD operations in  Friends Neo4j database

class FriendshipBuilderFRS(object):
    
    def __init__ (self):
      FriendshipBuilderFRS= self
       
    #load the users from csv to server database(500 records)
    def buildInitUserNodesFromCsvFRS(self):
        graphDatabase = GraphDatabase("http://beforecat.sb05.stations.graphenedb.com:24789/db/data/","beforecat","8ltlAVNJjyaEgW7s7AAp")
        try:
             
            with open("AU-import2.csv", "rb") as infile:
                reader = csv.reader(infile)
                next(reader, None)
                start = time.time()
                q = """MATCH (n) DETACH DELETE n"""
                graphDatabase.query(q=q)
                for row in  reader:
                    user = graphDatabase.labels.create("User")
                    print row[0]
                    property = graphDatabase.nodes.create(userId=self.strip(row[0]),firstName=self.strip(row[1]),email=self.strip(row[8]),cat1=self.strip(row[11]),cat2=self.strip(row[12]),cat3=self.strip(row[13]),cat4=self.strip(row[14]),cat5=self.strip(row[15]),cat6=self.strip(row[16]),cat7=self.strip(row[17]),cat8=self.strip(row[18]))
                    user.add(property)
                    
            
        finally:
            reader.close()
    
    #Build Sample network
    def buildSingleUserNetwork(self):
        lines  = [line.rstrip('\n') for line in open('convertedChat.txt')]
        for line in lines:
            item = line.split(";")
            friendEmail = item[1]
            self.makeNewFriendship("kalana331@gmail.com",friendEmail)
            print friendEmail
             
             

    #create the relationships between users in database refered to friendsNetwork3.txt
    def buildInitFriendsNetworkFRS(self):
         lines = [line.rstrip('\n') for line in open('friendsNetwork3.txt')]
         rowCount = 0
        
         for line in lines:
             nameArray = line.split(";")
             nameCount=0
             friends=[]
             user=""
             for name in nameArray:
                 if(nameCount==0):
                     user=name
                     nameCount =nameCount+1
                     
                 else:   
                     friends.append(name)
                     nameCount =nameCount+1
             rowCount = rowCount+1
             
             for friend in friends:
                 
                 if(friend != name):
                    print "USER:"+name+"-[friend_of]->"+friend
                    self.makeNewFriendship(name,friend)



   #Remove friendship  between two nodes 
   #Order does not matter what ever [:FRIEND_OF] type connection gets destroyed
    def removeExistingRelationship(self, email1,email2):
        try:
            isFriend = self.checkExistingFriendshipFRS(email1,email2)
            status =False
            if isFriend == 1:
                #authenticate("localhost:7474","neo4j","neo4j")
                graph = Graph("http://beforecat:8ltlAVNJjyaEgW7s7AAp@beforecat.sb05.stations.graphenedb.com:24789/db/data/")       
                batch = graph.cypher.begin()
                query = """START n=node(*) MATCH n-[rel:FRIEND_OF]-r WHERE n.email='"""+email1+"""' AND r.email='"""+email2+"""' DELETE rel"""
                batch.append(query,{"em1":email1,"em2":email2})
                batch.process()
                batch.commit()
                
            
        except Exception:
            return False
        finally:
            if isFriend ==1 :return True
            return False

    #Send a friend request to  a user
    #Create new [:REQUESTED] type connection
    def sendFriendRequestFRS(self,email1,email2):
        friendshipExists=self.checkExistingFriendshipFRS(email1,email2)
        alredyRequested = self.checkExistingRequestFRS(email1,email2)
        try:
            if friendshipExists == 0 and alredyRequested == 0 :
                
                #authenticate("localhost:7474","neo4j","neo4j")
                graph=Graph("http://beforecat:8ltlAVNJjyaEgW7s7AAp@beforecat.sb05.stations.graphenedb.com:24789/db/data/")
                batch = graph.cypher.begin()     
                query = """MATCH (u1:User {email:'"""+email1+"""'}), (u2:User{email:'"""+email2+"""'}) CREATE (u1)-[:REQUESTED{strength:0}]->(u2)"""
                batch.append(query,{"email1":email1,"email2":email2})
                batch.process()
                batch.commit()
        except Exception:
            return False
        finally:
            if friendshipExists == 0 and alredyRequested == 0 :
                return True
            else : return False
        

    #Cancel a friend request
    def cancelFriendRequestFRS(self,sender,reciver):
        alredyRequested = self.checkExistingRequestFRS(sender,reciver)
        try:
            if alredyRequested ==1:
                #authenticate("localhost:7474","neo4j","neo4j")
                graph=Graph("http://beforecat:8ltlAVNJjyaEgW7s7AAp@beforecat.sb05.stations.graphenedb.com:24789/db/data/")
                batch = graph.cypher.begin()
                query = """START n=node(*) MATCH n-[rel:REQUESTED]->r WHERE n.email='"""+sender+"""' AND r.email='"""+reciver+"""' DELETE rel"""          
                batch.append(query,{"sender":sender,"reciver":reciver})
                batch.process()
                batch.commit()
                return True
        except Exception:
            return False
        finally:
            if alredyRequested ==1:
               return True
            else :return False
    
   
    
          
    
        #Remove existing  [:REQUESTED] type connection and create [:FRIEND_OF] connection ;Build friendship
    def acceptNewFriendshipFRS(self,email1,email2):
        alredyRequested = self.checkExistingRequestFRS(email1,email2)
        isFriend = self.checkExistingFriendshipFRS(email1,email2)
        cancelSts=False
        makeSts=False
        if alredyRequested ==1 and isFriend ==0: 
            
           cancelSts= self.cancelFriendRequestFRS(email1,email2)
           makeSts=self.makeNewFriendship(email1,email2) 
        if cancelSts ==True and makeSts == True:      
            return True
        else: return False

    #Make a friendship between two nodes
    def makeNewFriendship(self,email1,email2):
        try:
            #authenticate("localhost:7474","neo4j","neo4j")
            graph=Graph("http://beforecat:8ltlAVNJjyaEgW7s7AAp@beforecat.sb05.stations.graphenedb.com:24789/db/data/")       
            batch = graph.cypher.begin()
            now = datetime.datetime.now()
           
            query = """MATCH (u1:User {email:'"""+email1+"""'}), (u2:User{email:'"""+email2+"""'}) MERGE (u1)-[:FRIEND_OF{strength:0,pvotes:0,nvotes:0,chats:0,duration:0,started:'"""+str(now)+""""'}]->(u2)"""
            batch.append(query,{"em1":email1,"em2":email2})
            batch.process()
            batch.commit()
            return True
        except Exception:
            return False
        finally: return True

    #Returns 1 [:FRIEND_OF] conn exists; 0 if not exists ; -1 for exception
    def checkExistingFriendshipFRS(self,userEmail,friendEmail):
        try:
            graphDatabase = GraphDatabase("http://beforecat.sb05.stations.graphenedb.com:24789/db/data/","beforecat","8ltlAVNJjyaEgW7s7AAp")
            response = 0
            query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where  su.email='"+friendEmail+"' AND fu.email ='"+userEmail+"' return fu,su"
            results = graphDatabase.query(query,returns = (client.Node,client.Node))
            for r in results:
                if r[1]["email"] != "":
                   response =1
                   return response
            
            
        except Exception:
            response =-1
            return response
        finally:
            return response

    #Returns 1 [:FRIEND_OF] conn exists; 0 if not exists ; -1 for exception
    def checkExistingRequestFRS(self,senderEmail,reciverEmail):
        try:
            graphDatabase = GraphDatabase("http://beforecat.sb02.stations.graphenedb.com:24789/db/data/","beforecat","8ltlAVNJjyaEgW7s7AAp")
            response = 0
            query = "MATCH (fu:User)-[rel:REQUESTED]->(su:User) Where  su.email='"+reciverEmail+"' AND fu.email ='"+senderEmail+"' return fu,su"
            results = graphDatabase.query(query,returns = (client.Node,client.Node))
            for r in results:
                if r[1]["email"] != "":
                   response =1
                   return response
            
            
        except Exception:
            response =-1
            return response
        finally:
            return response
          
        

    # Returns select  all  friends of user
    def selectAllFriends(self,email):
        
        graphDatabase = GraphDatabase("http://beforecat.sb02.stations.graphenedb.com:24789/db/data/","beforecat","8ltlAVNJjyaEgW7s7AAp")
        query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where  rel.strength=0 AND fu.email ='"+email+"' return  su,rel.strength"
        results =  graphDatabase.query(query,returns = (client.Node,str,client.Node))
        json_object = []
        for r in results:
            element={}
            element['email']=r[0]["email"]
            element['userId']=r[0]["userId"]
            element['strength'] =r[1]
            json_object.append(element)
                       
        if len(json_object)!=0:
            return json.dumps(json_object)
        else:return 0

    def getAllFriendRecievedRequests(self,email):
        graphDatabase = GraphDatabase("http://beforecat.sb02.stations.graphenedb.com:24789/db/data/","beforecat","8ltlAVNJjyaEgW7s7AAp")
        query = "MATCH (fu:User)<-[rel:REQUESTED]-(su:User) Where  rel.strength=0 AND fu.email ='"+email+"' return fu, type(rel), su,rel.strength"
        results =  graphDatabase.query(query,returns = (client.Node,str,client.Node,str))
        json_object=[]
        for r in results:
           
           #print "(%s)-STRENGTH:%s" % (r[2]["email"],r[3])
           element={}
           element['email']=r[2]["email"]
           element['userId']=r[2]["userId"]
           json_object.append(element)
        if len(json_object)!=0: return json.dumps(json_object)
        else : return 0
    
        # Return list of Pending requests 
    def getAllPendingFriendRequests(self,email):
        graphDatabase = GraphDatabase("http://beforecat.sb02.stations.graphenedb.com:24789/db/data/","beforecat","8ltlAVNJjyaEgW7s7AAp")
        query = "MATCH (fu:User)-[rel:REQUESTED]->(su:User) Where  fu.email ='"+email+"' return fu, su,rel.strength"
        results =  graphDatabase.query(query,returns = (client.Node,client.Node,str))
        json_object = []
        for r in results:
           element={}
           element['email']=r[1]["email"]
           element['userId']=r[1]["userId"]
           element['strength']=r[2]
           json_object.append(element)
        if len(json_object)!=0: return json.dumps(json_object)
        else:return 0
         

#removes non utf-8 chars from string within cell
    def strip(self,string):
        return''.join([c if 0 < ord(c) < 128 else ' ' for c in string]) 

    









    

 


