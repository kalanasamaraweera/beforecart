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
import logging.handlers
import subprocess
import ast
import sys
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
                
        #Data Access
        sMgr = SuggestionManagerFRS()
        uMgr = UserManagerFRS()

        #get user email
        email = uMgr.getUserEmail(str(userId))

        if email != '' and int( userId) != 0: #validate request
            
            print (" Invoked suggest_new_pals_frs in FriendshipHandlerFRS.py \n TIME :"+ str(datetime.datetime.today())+"\n Returned:\n")
            #get list of users
            list = []
            users = sMgr.suggestNewFriends(email)
            for user in users: 
                #filter required fields of user
                print("User:"+str(user))
                item ={}               
                item['firstname']= user['firstName']
                item['email']= user['email']
                item['userId'] =user['userId']
                list.append(item) 
            #write results            
            self.write(json.dumps(list))
        else:
            print ("Invalid userID or couldn't refine email;\n userId:"+str(userId)+" email="+str(email))
            self.set_status(400)
            self.write_error(400) 

#suggest freinds for chat
class SuggestFriendsForChatFRS(tornado.web.RequestHandler):
    def get(self):
        
          
        userId = self.get_argument('userId','0') #userid
        catId  =self.get_argument('catId','0') #product category id

        #check userid and catid
        if int(userId) > 0 and 0<int(catId)<9:

            sMgr = SuggestionManagerFRS()
            uMgr =UserManagerFRS()

             #get user email
            email = uMgr.getUserEmail(str(userId))
            #check email
            if str(email) != '':

              #get suggestion list
              suggestedList= sMgr.refineChatList(email,str(catId))
              print ("response: 200- Results:\n"+str(suggestedList))
              self.write(json.dumps(suggestedList))
              return

            #invalid email
            else:
               print("Invalid Email ;\n userId:"+str(userId))
               self.set_status(400)
               return   self.write_error(400)                    
            
        else:
            print ("Invalid userID or catId ;\n userId:"+str(userId))
            self.set_status(400)


#save a concluded chat data in db
class saveNewChatFRS(tornado.web.RequestHandler):

    #post method
    def post(self):
        friends =''
        userId = ''
        chatData =''
        try:
        # fetch  get user,freinds,conversation data to dictionary
            data =json.loads(str(self.request.body))
            list ={}
            for slot in  data:
              
              list.update({str(slot):str(data[slot])})
           

            print list
            userId= list['userId']
            friends=list['friend']
            chatData= list['chat']
            
            friends = ast.literal_eval(friends)


        except Exception ,e:
            print e.message
            self.write_error(500)
        finally:
            #if data is not empty
            if userId !='' and friends !='' and chatData != '':

                #invoke data access
                uMgr  = UserManagerFRS()
                cMgr = ChatHistoryFRS()

                #get user email 
                email = uMgr.getUserEmail(userId)

                #if email is not empty
                if email != '':

                    #save chat
                    result=cMgr.saveChatHistoryFRS(email,friends,chatData)

                    # if chat saved successfully
                    if result==True:
                        print ('chat saved successfully')
                        self.write('200')
                    else:
                        print ('chat did not saved server error')
                        self.write_error(500)
                else:
                    self.write_error(500)
            else:
                print 'invalid data'
                self.write_error(500)
    
    #get method
    def get(self):
        print ('get method is not supported')
        self.write_error(500)



class BeforeCartAPI(tornado.web.Application):
    def __init__(self):
        handlers = [
            #FRS service handlers
                (r"/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/chatlist/?",SuggestFriendsForChatFRS),
                (r"/beforecart/frs/newfriends/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/savechat/?",saveNewChatFRS)
            ]
        tornado.web.Application.__init__(self,handlers)





def main():

    app = BeforeCartAPI() #application
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
        
        main()