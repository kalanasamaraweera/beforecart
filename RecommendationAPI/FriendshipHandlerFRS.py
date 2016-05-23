
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
            '/chatpals/(.*)/(.*)' , 'suggest_for_chat_frs'   #FRS
         )


application =web.application(routes,globals())

'FRS Service calls implemented  below'

#pick friends to make new relationships

class suggest_new_pals_frs:

    def GET(self,userId):

        logging.basicConfig(filename='log.txt',level=logging.DEBUG)
        sMgr = SuggestionManagerFRS()
        uMgr =UserManagerFRS()

        email = uMgr.getUserEmail(userId)
        if email != '':
            users = sMgr.suggestNewFriends(email)
            list =[]

            logging.info(" Invoked suggest_new_pals_frs in FriendshipHandlerFRS.py \n TIME :"+ str(datetime.datetime.today())+"\n Returned:\n")
            for user in users:
            
                logging.info(str(user))
                item ={}
                item['firstname']= user['firstName']
                item['email']= user['email']
                item['userId'] =user['userId']
                list.append(item)
            return json.dumps(list)
        else:
            logging.error('suggestNewFriends(email) returned nothing.\n Cannot make suggestions to empty email address ')
            list = []
            return list

#pick friends for chat

'FRS Service calls ends'

if __name__=="__main__":
    application.run()