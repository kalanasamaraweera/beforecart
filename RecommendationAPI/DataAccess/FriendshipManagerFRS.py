from  neo4jrestclient.client import GraphDatabase
from DataAccess import UserManagerFRS
from py2neo import Graph ,authenticate 
from DataAccess import DBConf

from neo4jrestclient import client
from datetime import timedelta as td
from datetime import datetime as date
import csv
import time
import datetime
import random
import json

#FriendshipBuilderFRS class implements CRUD operations in  Friends Neo4j database

class FriendshipManagerFRS(object):
    
    def __init__ (self):
      FriendshipManagerFRS= self
    
      #change positive votes  by one
    def changePosVotes(self,user,friend,operation):
        try:
            rel =self.selectRelationship(user,friend)
            pVotes=int(rel[2])
            if len(rel)==5:

                

                if operation == '+': 
                    pVotes+=1
                    self.upgradeRelationship(user,friend,"pvotes",pVotes)

                elif operation == '-':
                    if pVotes>=1:
                        pVotes-=1
                        self.upgradeRelationship(user,friend,"pvotes",pVotes)
                    
                else:return -1

        except Exception ,e:
            print e.message  
            return -1

        finally:
            if operation =='+' or operation =='-':
                if pVotes >=1:
                    return 0
                return -1
            else : return -1

    #change negative votes by one
    def changeNegVotes(self,user,friend,operation):
        try:
            rel=self.selectRelationship(user,friend)
            nVotes=int(rel[3])
            
            if len(rel)==5:

                if operation =='+':

                    nVotes+=1
                    self.upgradeRelationship(user,friend,"nvotes",nVotes)
                    
                elif operation == '-':
                    if nVotes>=1:
                        nVotes-=1
                        self.upgradeRelationship(user,friend,"nvotes",nVotes)
                    
                else: return -1
           

        except Exception ,e:
            print e.message
            return -1
        finally:
            if operation =='+' or operation =='-':
                if nVotes>=1:
                    return 0
                return -1
            else : return -1


      # get random date
    def getRandomDate(self):
        
        createdDayCount  =  random.uniform(365,730)
        lastUpdatedDayCount = random.uniform(100,250)
        #today  =  datetime.date.today()  #only date    
        today  =  datetime.datetime.today() #Entire date & time
        createdGap = td(days =createdDayCount)
        updatedGap = td(days=lastUpdatedDayCount)

        createdDate= today-createdGap
        days= updatedGap.days #print days
        lastedUpdatedDate = today -updatedGap

        dateArray ={}
        dateArray[0]= str(createdDate)
        dateArray[1]=str(lastedUpdatedDate)
        dateArray[2]=days

        return dateArray


      
    # Increase friendship duration
    def increaseDuration(self,userEmail):
        
        #db config
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()
        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
        
        #get user id
        userMgr = UserManagerFRS.UserManagerFRS()
        userId = userMgr.getUserId(userEmail)
        try:
            #get friendship duration
            query = "MATCH (fu:User)-[rel:FRIEND_OF]->(su:User) WHERE fu.userId="+str(userId)+"  RETURN rel.duration,su.email"
            result = graphDatabase.query(query,returns = (str,str))
            today =datetime.datetime.today()
            
            for item in result:
                 
                dur =int(item[0])+1
                print("%s"%str(item[1]))
                print (str(item[0])+"->"+str(dur))

                #update
                self.upgradeRelationship(userEmail,item[1],"duration",dur)
                


        except Exception ,ex:
            print(ex.message)
            return False


   


        

       
    #load the users from csv to server database(500 records)
    def buildInitUserNodesFromCsvFRS(self):
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
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
    
    #Build Friendships between main user and friends
    def buildSingleUserNetwork(self):
        
        lines  = [line.rstrip('\n') for line in open('convertedFriends.txt')]
        mainUser="kalana331@gmail.com"
        
        for line in lines:
            item = line.split(";")
            friendEmail = item[1]
            self.removeExistingRelationship(mainUser,friendEmail)
            

            
            self.makeNewFriendship(mainUser,friendEmail)

            #update votes
            pvotes  =  random.uniform(0,100)
            nvotes = random.uniform(0,100)
            self.upgradeRelationship(mainUser,item[1],"pvotes",int(pvotes))
            self.upgradeRelationship(mainUser,item[1],"nvotes",int(nvotes))

            #self.upgradeRelationship(mainUser,item[1],"strength",random.uniform(0,0.99))
            #update chats
            self.upgradeRelationship(mainUser,item[1],"chats",item[3])

            dateArray= self.getRandomDate()
            #update friendship  duration
            self.upgradeRelationship(mainUser,item[1],"duration",str(dateArray[2]))

            #update  friendship started date
            self.upgradeRelationship(mainUser,item[1],"started",dateArray[0])

            #update  friendship started date
            self.upgradeRelationship(mainUser,item[1],"triggered",dateArray[1])

            print(str(mainUser)+"->"+str(friendEmail))
            print ("Since"+str(dateArray[0]))
            print ("Updated on "+str(dateArray[1])+" ; before"+str(dateArray[2])+" days")
            
             
             
    

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
                conf = DBConf.DBConf()
                element=conf.getNeoGraphConfig()

                graph = Graph(element)       
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

                conf = DBConf.DBConf()
                element=conf.getNeoGraphConfig()

                graph = Graph(element)
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
                conf = DBConf.DBConf()
                element=conf.getNeoGraphConfig()

                graph = Graph(element)
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
            conf = DBConf.DBConf()
            element=conf.getNeoGraphConfig()

            graph = Graph(element)       
            batch = graph.cypher.begin()
            now = datetime.datetime.now()
           
            query = """MATCH (u1:User {email:'"""+email1+"""'}), (u2:User{email:'"""+email2+"""'}) MERGE (u1)-[:FRIEND_OF{strength:0,pvotes:0,nvotes:0,chats:0,duration:0, triggered:'"""+str(now)+""""', started:'"""+str(now)+""""'}]->(u2)"""
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
            elements =[]
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()

            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
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
            elements =[]
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()

            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
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
          
        

    # Returns select  all  friends of user and relationship info
    def selectAllFriends(self,email):
        
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
        query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where   fu.email ='"+email+"' RETURN  su.email,rel.strength,rel.duration,rel.chats order by toFloat(rel.strength) desc"
        try:
            results =  graphDatabase.query(query,returns = (str,str,str,str))
            json_object = []
            for r in results:
                element={}
                element['email']=r[0]
                
                element['strength'] =r[1]
                element['duration']= r[2]
                element['chats']= r[3]
                json_object.append(element)
                
        
        except Exception ,ex:
            print ex.message
            return 0
        finally:               
            if len(json_object)!=0:
                return json_object
            else:return 0

    #select friends for Chat
    def selectFriendsForChatOnExp(self,email,cat):
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
        query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where fu.email ='"+email+"' RETURN  su.email,rel.strength,su."+cat+" order by su."+cat+"  desc"
        try:
            results =  graphDatabase.query(query,returns = (str,str,str))
            json_object = []
            for r in results:
                element={}
                element['email']=r[0]
                element['strength'] =r[1]
                element[str(cat)]= r[2]
                json_object.append(element)
                
        
        except Exception ,ex:
            print ex.message
            return 0
        finally:               
            if len(json_object)!=0:
                return json_object
            else:return 0

 
 
    #Returns expertised level for product category of friends
    def selectExpertiseOfFriends(self,userEmail,category):
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
        query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where  rel.strength=0 AND fu.email ='"+userEmail+"' return  su."+category+",su.email order by su."+category+" desc"
        results =  graphDatabase.query(query,returns = (str,str))
        json_object = []
        for r in results:
            element={}
            element['exp']=r[0]
            element['email']=r[1]

            json_object.append(element)
                       
        if len(json_object)!=0:
            return json.dumps(json_object)
        else:return 0

    #Returns friends of freinds of an user node sorted in descending order for given product category
    def selectFriendsForFriendship(self, email,category):
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
        query= "match (u:User{email:'"+email+"'})-[rel1:FRIEND_OF]-(m)-[rel2:FRIEND_OF]-(n:User) where NOT (n)-[:FRIEND_OF]-(u) return distinct id(n) as Id,n,n.userId,n.email,n.firstName,n."+category+"  order by n."+str(category)+" desc"
        results =  graphDatabase.query(query,returns = (str,client.Node,str,str,str))
        candidates =[]
        for r in results:
            
            #print str( r[2])+"->"+str(r[4])
            try:
                user ={}
                user['userId']=r[2]
                user['email'] =r[3]
                user['firstName']= r[4]
                user[str(category)]= float( r[5])
                
            except Exception,e:
                print e.message
                continue
            finally:
                #print user
                candidates.append(user)

        return candidates


            

    #select relationship
    def selectRelationship(self,user,friend):
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
        query = "MATCH (fu:User)-[rel:FRIEND_OF]-(su:User) Where  fu.email ='"+user+"' AND  su.email='"+friend+"' return rel.chats, rel.duration,rel.pvotes,rel.nvotes,rel.strength"
        try:
            results =  graphDatabase.query(query,returns = (str,str,str,str,str))
            list = []
            for i in results:
                list.append(i[0])
                list.append(i[1])            
                list.append(i[2])          
                list.append(i[3])
                list.append(i[4])   
                          
        except Exception,ex:
            print ex.message
            elements=[]
            return  elements
        finally:return list
                       



    
    def getAllFriendRecievedRequests(self,email):
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
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
        elements =[]
        conf = DBConf.DBConf()
        elements =  conf.getNeo4jConfig()

        graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
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

    #Upgrade the edge properties between  two user nodes
    def upgradeRelationship(self,userEm,friendEm,param,val):
        try:
            email = ''
            elements =[]
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()
            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])
            query = "MATCH (fu {email:'"+str(userEm)+"'})-[rel:FRIEND_OF]-(su{email:'"+str(friendEm)+"'}) SET rel."+str(param)+"='"+str(val)+"' RETURN fu.email"
            results= graphDatabase.query(query,returns = (str))
           
            for result in results:
                email = result[0]

        except Exception ,ex:
            print str(ex.message)
            return False
        finally:
            if email == userEm:return True
            else:return  False

    #increase chat count
    def increaseChatCount(self,user,friend):

        #get chat count
        
        results = self.selectRelationship(user,friend)

        try:
            chats=0
            if len(results) !=0:
                chats=int(results[0])

        except Exception ,ex:
            print ex.message
            return 0
        #save new chat count in neo4j
        finally:
            chats+=1
            return self.upgradeRelationship(user,friend,"chats",chats)


    #return all the category exp values of each friend with  relationship strength
    def getFriendAllExpList(self,email):
        try:
            elements =[]
            conf = DBConf.DBConf()
            elements =  conf.getNeo4jConfig()
            graphDatabase = GraphDatabase(elements[0],elements[1],elements[2])

        except Exception,e:
            print  e.message
            return False

        finally:
            
            query = "match (n)-[rel:FRIEND_OF]-(m) where n.email='"+email+"' return m.cat1,m.cat2,m.cat3,m.cat4,m.cat5,m.cat6,m.cat7,m.cat8,rel.strength,m.userId"
            
            try:
                friends =[]
                results= graphDatabase.query(query,returns = (str,str,str,str,str,str,str,str,str,str))
                for r in results:

                    categories ={} #prepare category expertise dictionary
                    categories['cat1']=r[0]
                    categories['cat2']=r[1]
                    categories['cat3']=r[2]
                    categories['cat4']=r[3]
                    categories['cat5']=r[4]
                    categories['cat6']=r[5]
                    categories['cat7']=r[6]
                    categories['cat8']=r[7]

                    mean =self.calculateCumulativeExpScore(categories) #calculate mean  for product expertise

                    friend ={}
                    friend['mean'] =mean
                    friend['strength']=float(r[8])*100
                    friend['userId']=  r[9]
                    
                    
                    friends.append(friend)

            except Exception,e:
                print e.message
                return False

        #print friends    
        return friends
    
    #calculate mean expertise for all product categories
    def calculateCumulativeExpScore(self,categories):
        mean= 0.0 
        if len(categories)==8:
            
            amount = 8.0 # product categories
            
            cat1 = float(categories['cat1'])
            cat2 = float(categories['cat2'])                   
            cat3 = float(categories['cat3'])
            cat4 = float(categories['cat4'])
            cat5 = float(categories['cat5'])
            cat6 = float(categories['cat6'])
            cat7 = float(categories['cat7'])
            cat8 = float(categories['cat8'])

            mean = float((cat1+cat2+cat3+cat4+cat5+cat6+cat7+cat8)/amount)*100
        return mean

#removes non utf-8 chars from string within cell
    def strip(self,string):
        return''.join([c if 0 < ord(c) < 128 else ' ' for c in string]) 

    









    

 


