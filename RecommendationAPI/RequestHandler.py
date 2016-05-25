import os
import sys
import tornado
import pymongo
from tornado.options import  options
from tornado import ioloop, web
from tornado.options import define
import json, traceback
from bson.objectid import ObjectId
#from indico.error import IndicoError, RouteNotFound, ServerError
#from indico.utils import LOGGER
from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import logging
import datetime

from DataAccess import FriendshipManagerFRS
from DataAccess import SuggestionManagerFRS
from DataAccess import ChatHistoryFRS
from DataAccess import UserManagerFRS 
from DataAccess import DBConf

#recommends uses to make relationships
class SuggestNewFriendsFRS(tornado.web.RequestHandler):
    def get(self):
        userId = self.get_argument('userId','0')
        #define logging
        logging.basicConfig(filename='log.txt',level=logging.DEBUG)        
        #Data Access
        sMgr = SuggestionManagerFRS()
        uMgr = UserManagerFRS()

        #get user email
        email = uMgr.getUserEmail(str(userId))
        logging.info(" Invoked suggest_new_pals_frs in FriendshipHandlerFRS.py \n TIME :"+ str(datetime.datetime.today())+"\n Returned:\n")
        #get list of users
        list = []
        users = sMgr.suggestNewFriends(email)
        for user in users: 
            #filter required fields of user
            logging.info(str(user))
            item ={}               
            item['firstname']= user['firstName']
            item['email']= user['email']
            item['userId'] =user['userId']
            list.append(item) 
        #write results            
        self.write(json.dumps(list))


#suggest freinds for chat
class SuggestFriendsForChatFRS(tornado.web.RequestHandler):
    def get(self):
        userId = self.get_argument('userId','0')



class BeforeCartAPI(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/chatlist/?",SuggestFriendsForChatFRS),
                (r"/beforecart/frs/newfriends/?",SuggestNewFriendsFRS)
            ]
        tornado.web.Application.__init__(self,handlers)




def main():

    app = BeforeCartAPI() #application
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
        main()