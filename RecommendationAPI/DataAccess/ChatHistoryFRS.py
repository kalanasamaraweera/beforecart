import pymongo
import datetime  
from bson.objectid import ObjectId
import json
from pprint import pprint
from DataAccess import FriendshipManagerFRS
from DataAccess import SuggestionManagerFRS
import datetime

from DataAccess import DBConf
class ChatHistoryFRS(object):

       
    def __init__(self):
       ChatHistoryFRS =self
  
    #Save chat data set in server database
    def saveChatHistoryFRS(self,userEmail,friendArr,conv):
        
        # sample chat template

        CHAT_DATA = [           
                {
                    'email':userEmail,
                    'friend':friendArr,
                    'time':str(datetime.datetime.today()),
                    'data':conv
                    
                }
                            
                    ]

        # Mongo Database configs

        conf = DBConf.DBConf()
        elements=conf.getMongoConf()
        client  = pymongo.MongoClient(elements[0])
        db = client.get_default_database()

        #Select database to save chat data
        chatDatabase = db['beforecart_chat_history']
        
        # Insert Sample Chat Data 
       #chatDatabase.insert(CHAT_DATA)

        if len(friendArr)>1: # if multiple friends

            for id,friend in friendArr.iteritems():

                #Update properties 
                time = datetime.datetime.today()
                try:
                    fBuild = FriendshipManagerFRS()
                    fBuild.upgradeRelationship(userEmail,friend,"triggered",str(time))
                    fBuild.upgradeRelationship(userEmail,friend,"duration",str(0))
                    fBuild.increaseChatCount(userEmail,friend)
                    #update friendship score
                    sugMgr = SuggestionManagerFRS.SuggestionManagerFRS()
                    score=sugMgr.makeFriendshipScore(userEmail,friend)
                    
                    if score != -1:
                        print "\n Score %s"%score
                        fBuild.upgradeRelationship(userEmail,friend,"strength",str(score))

                    

                except Exception,e:
                    print e.message
                    continue
                


        else:   #Update relationship properties
                time = datetime.datetime.today()
                try:
                    fBuild = FriendshipManagerFRS()
                    fBuild.upgradeRelationship(userEmail,friendArr,"triggered",str(time))
                    fBuild.upgradeRelationship(userEmail,friendArr,"duration",str(0))
                    fBuild.increaseChatCount(userEmail,friendArr)
                    sugMgr = SuggestionManagerFRS.SuggestionManagerFRS()
                    score=sugMgr.makeFriendshipScore(userEmail)
                    fBuild.upgradeRelationship(userEmail,friendArr,"strength",str(score))
                    print "/n Score %s"%str(score)
                    print userEmail+"-"+friendArr

                except Exception,e:
                    print e.message



        
                  
        #Return chat history of user
    def getAllChatsOfUser(self,email):

        conf = DBConf.DBConf()
        elements=conf.getMongoConf()
        client  = pymongo.MongoClient(elements[0])
        db = client.get_default_database()

        #Select database to retrieve chat data
        chatDatabase = db['beforecart_chat_history']

       # query = {"userId": "1"}
        cursor = chatDatabase.find({'email':{'$eq':email}}).sort('date',1)
        list =[]
        for doc in cursor:
          friends= doc['friends']
          time =  doc['time']
          list.append({'time':time,'friends':friends})
       
        return list

    #Convert Auctual names to fake names
    def convertSampleChat(self):

        documentArray = [line.rstrip('\n') for line in open('convertedFriends.txt')]
        ucount=0

        #per each line in document
        for line in documentArray:

            elementArray = line.split(';') 
            oldName = elementArray[2]
            newName = elementArray[1]
            oldName ="\""+oldName+"\""
            newName ="\""+newName+"\""
            ucount=ucount+1

            if int(elementArray[3])> 0:

                print ucount
                f =  open('Messages.txt','r')
                data = f.read()
                
                newData = data.replace(oldName,newName)

                f = open('Messages.txt','w')
                f.write(newData)
                f.close()
                


    #Save Sample Chat History in Database 

    def saveSampleChatData(self):
         
        
            documentArray = [line.rstrip('\n') for line in open('convertedFriends.txt')]
            doc=  [line.rstrip('\n') for line in open('Replace.txt')]
            #messageData
            myEmail =  "kalana331@gmail.com"

            for name  in documentArray:
                chatCount = 0
                name = name.split(";")

                for line in doc:

                    if line.find(name[1]) != -1  and  name!=myEmail and name[3]>0:
                        chatCount+=1
                        print "Found=> "+ str(name[1])

                        try:

                            lineArray = line.split(",")
                            datestr(lineArray[1])+str(lineArray[2])
                            friend = name[1]
                            message=[{"User":'What\'s this\?'},{friend:'It \'s  a shirt'}]
                            self.saveChatHistoryFRS(myEmail,friend,date,message)


                        except Exception,ex:
                            print ex.message
                            continue

                    else:continue
                



        
                    
                    

                
                    










            


            


    

   


    


