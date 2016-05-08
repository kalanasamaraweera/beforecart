from  neo4jrestclient.client import GraphDatabase
from py2neo import Graph ,authenticate 
from neo4jrestclient import client
import csv
import time

class FriendshipBuilderFRS(object):
    
    def __init__ (self):
      FriendshipBuilderFRS= self
       
    #load the users from csv to server database(500 records)
    def fillUserNodesFromCsvFRS(self):
        graphDatabase = GraphDatabase("http://localhost:7474","neo4j","neo4j")
        try:
             
            with open("AU-import2.csv", "rb") as infile:
                reader = csv.reader(infile)
                next(reader, None)
                start = time.time()
                q = """MATCH (n) DETACH DELETE n"""
                graphDatabase.query(q=q)
                for row in  reader:
                    user = graphDatabase.labels.create("User")
                    property = graphDatabase.nodes.create(userId=self.strip(row[0]),firstName=self.strip(row[1]),email=self.strip(row[8]),cat1=self.strip(row[11]),cat2=self.strip(row[12]),cat3=self.strip(row[13]),cat4=self.strip(row[14]),cat5=self.strip(row[15]),cat6=self.strip(row[16]),cat7=self.strip(row[17]),cat8=self.strip(row[18]))
                    user.add(property)
                    print row[0]
            
        finally:
            reader.close()

   #Remove friendship  between two nodes 
   #Order does not matter what ever [:FRIEND_OF] type connection gets destroyed
    def removeExistingRelationship(self, email1,email2):
        authenticate("localhost:7474","neo4j","neo4j")
        graph = Graph("http://localhost:7474/db/data/")       
        batch = graph.cypher.begin()
        query = """START n=node(*) MATCH n-[rel:FRIEND_OF]-r WHERE n.email='"""+email1+"""' AND r.email='"""+email2+"""' DELETE rel"""
        batch.append(query,{"em1":email1,"em2":email2})
        batch.process()
        batch.commit()

    #Send a friend request to  a user
    #Create new [:REQUESTED] type connection
    def sendFriendRequestFRS(self,email1,email2):

        self.cancelRequestByRecieverFRS(email1,email2)
        authenticate("localhost:7474","neo4j","neo4j")
        graph=Graph("http://localhost:7474/db/data/")
        batch = graph.cypher.begin()     
        query = """MATCH (u1:User {email:'"""+email1+"""'}), (u2:User{email:'"""+email2+"""'}) CREATE (u1)-[:REQUESTED{strength:0}]->(u2)"""
        batch.append(query,{"em1":email1,"em2":email2})
        batch.process()
        batch.commit()

    #Cancel a friend request
    def cancelFriendRequestBySenderFRS(self,email1,email2):
        authenticate("localhost:7474","neo4j","neo4j")
        graph=Graph("http://localhost:7474/db/data/")
        batch = graph.cypher.begin()
        query = """START n=node(*) MATCH n-[rel:REQUESTED]->r WHERE n.email='"""+email1+"""' AND r.email='"""+email2+"""' DELETE rel"""          
        batch.append(query,{"em1":email1,"em2":email2})
        batch.process()
        batch.commit()
    
    #In here  sequence of em1,em2 does not matter what ever [:REQUESTED] type connection gets destroyed
    def cancelRequestByRecieverFRS(self,email1,email2):
        authenticate("localhost:7474","neo4j","neo4j")
        graph=Graph("http://localhost:7474/db/data/")
        batch = graph.cypher.begin()
        query = """START n=node(*) MATCH n-[rel:REQUESTED]-r WHERE n.email='"""+email1+"""' AND r.email='"""+email2+"""' DELETE rel"""          
        batch.append(query,{"em1":email1,"em2":email2})
        batch.process()
        batch.commit()
         
    #Remove existing  [:REQUESTED] type connection and create [:FRIEND_OF] connection
    def acceptNewFriendshipFRS(self,email1,email2):
        self.cancelRequestByRecieverFRS(email1,email2)
        self.makeNewFriendship(email1,email2)   
       
        

    #Make a friendship between two nodes
    def makeNewFriendship(self,email1,email2):

        authenticate("localhost:7474","neo4j","neo4j")
        graph=Graph("http://localhost:7474/db/data/")       
        batch = graph.cypher.begin()
        query = """MATCH (u1:User {email:'"""+email1+"""'}), (u2:User{email:'"""+email2+"""'}) CREATE (u1)-[:FRIEND_OF{strength:0}]->(u2)"""
        batch.append(query,{"em1":email1,"em2":email2})
        batch.process()
        batch.commit()

    #Returns 1 [:FRIEND_OF] conn exists; 0 if not exists ; -1 for exception
    def checkExistingFriendshipFRS(self,userEmail,friendEmail):
        try:
            graphDatabase = GraphDatabase("http://localhost:7474","neo4j","neo4j")
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

          
        

    # Returns select  all  friends of user
    def selectAllFriends(self,email):
        
        graphDatabase = GraphDatabase("http://localhost:7474","neo4j","neo4j")
        query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where  rel.strength=0 AND fu.email ='"+email+"' return fu, type(rel), su,rel.strength"
        results =  graphDatabase.query(query,returns = (client.Node,str,client.Node))
        for r in results:
            #print  "(%s)-[%s]->(%s)" % (r[0]["email"],r[1],r[2]["email"])
            print "(%s)-STRENGTH:%s" % (r[2]["email"],r[3])


    
    



    def strip(string):
        return''.join([c if 0 < ord(c) < 128 else ' ' for c in string]) #removes non utf-8 chars from string within cell

    









    

 


