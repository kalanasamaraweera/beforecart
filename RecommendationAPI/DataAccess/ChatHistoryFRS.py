import pymongo
import datetime  
from bson.objectid import ObjectId
class ChatHistoryFRS(object):

    MONGODB_URI = 'mongodb://kalana:ys2b7iiway@ds023052.mlab.com:23052/beforecart_chat_history'   
    def __init__(self):
       ChatHistoryFRS =self
  
    #Save chat data set in server database
    def saveChatHistoryFRS(self,userEmail,friendArr,conversation):
        
        ### sample chat DATA

        CHAT_DATA = [
            
                {
                    'email':userEmail,
                    'friends':friendArr,
                    'time': datetime.datetime.now(),
                    'conv':conversation
                    
                }
                            
                    ]

        ### Database location

       
        client  = pymongo.MongoClient(self.MONGODB_URI)

        db = client.get_default_database()

        #Select database to save chat data

        chatDatabase = db['beforecart_chat_history']
        
        ## Insert Sample Chat Data 

        chatDatabase.insert(CHAT_DATA)




    
        #Return chat history of user

    def getAllChatsOfUser(self,email):

        client  = pymongo.MongoClient(self.MONGODB_URI)

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

    

   


    


