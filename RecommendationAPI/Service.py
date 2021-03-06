
from DataAccess import FriendshipManagerFRS
from DataAccess import SuggestionManagerFRS
from DataAccess import ChatHistoryFRS
from DataAccess import UserManagerFRS 
from DataAccess import DBConf
import logging
import datetime

import web
import xml.etree.ElementTree as ET
import json

routes = (
            '/newpals/(.*)' , 'suggest_new_pals_frs',   #FRS
            '/chatpals/(.*)/(.*)' , 'suggest_for_chat_frs',   #FRS
            '/upgraderels/(.*)','upgrade_rels_frs'
         )


application =web.application(routes,globals())

'FRS Service calls implemented  below'

#pick friends to make new relationships

class suggest_new_pals_frs:

    def GET(self,userId):

        logging.basicConfig(filename='log.txt',level=logging.DEBUG) #initaite logging
        sMgr = SuggestionManagerFRS() # refer Data Access
        uMgr =UserManagerFRS()
        #get email for passed user id
        email = uMgr.getUserEmail(userId) 
        #if email is not empty
        if email != '': 
            users = sMgr.suggestNewFriends(email) #get suggested user list of new friends
            list =[]

            logging.info(" Invoked suggest_new_pals_frs in FriendshipHandlerFRS.py \n TIME :"+ str(datetime.datetime.today())+"\n Returned:\n")
            # for each user object in users list
            for user in users: 
                 #filter required fields of user
                logging.info(str(user))
                item ={}               
                item['firstname']= user['firstName']
                item['email']= user['email']
                item['userId'] =user['userId']
                list.append(item)
            return json.dumps(list)
        else:
            logging.error('getUserEmail(email) returned nothing.\n Cannot make suggestions to empty email address ')
            list = [{'ERROR':'Unable to find UserId in server'}]
            return json.dumps(list)

#pick friends for chat
class  suggest_for_chat_frs:
    
    def GET(self,userId,catId):

        logging.basicConfig(filename='log.txt',level=logging.DEBUG)
        catId=  int(catId)

        sMgr = SuggestionManagerFRS()
        uMgr =UserManagerFRS()

        email = uMgr.getUserEmail(str(userId))

        if email != '' and 0<catId<9:

             suggestedList= sMgr.refineChatList(email,str(catId))
             logging.info('suggest_for_chat_frs in FriendHandlerFRS invoked \n TIME:'+str(datetime.datetime.today())+"\n Response:\n"+str(suggestedList))
             
             return json.dumps(suggestedList)

        if email=='':
            logging.error('getUserEmail(Id) returned nothing.\n Cannot make suggestions to empty email address \n')
        
        if catId<=0 or catId>=9:
            logging.error('Invalid catId .\n The category id must me a value between [1-8]\n')
        list = [{'ERROR':'Could not process request'}]
        return json.dumps(list)
 
    
 #Upgrade relationships with all friends                    

'FRS Service calls ends'

if __name__=="__main__":
    application.run()