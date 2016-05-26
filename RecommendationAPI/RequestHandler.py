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
            print list            
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
              self.set_status(200)
              self.write(json.dumps(suggestedList))
              return

            #invalid email
            else:
               print("Invalid Email ;\n userId:"+str(userId))
               self.set_status(404)
               self.write_error(404)                    
            
        else:
            print ("Invalid userID or catId ;\n userId:"+str(userId))
            self.set_status(406)
            self.write_error(406)


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
            self.write_error(417)
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
                        self.write('1')
                    else:
                        print ('saving chat returned error.Chat saved with errors ')
                        self.write(417)
                else:
                    print 'Could not fnd matching email address .Chat did not saved in server '
                    self.write_error(404)
            else:
                print 'invalid data given Id'+str(userId)+","+str(datetime.datetime.today())
                self.write_error(203)
    
    #get method
    def get(self):
        print ('get method is not supported')
        self.write_error(501)

class CreateUserFRS(tornado.web.RequestHandler):
    #create new user
    def post(self):
        
        #retreive data
        data ={}
        #validate data
        username = self.get_argument('username','')
        if username != '':
            data['username'] = str(username)
        else:
            self.set_status(406)           
            self.write("username is empty")
            return 

        password = self.get_argument('password','')
        if password !='':
            data['password'] = str(password)
        else:
            self.set_status(406)           
            self.write('password is  empty')
            return 

        
        firstName = self.get_argument('firstName','')
        if firstName != '':
            data['firstName'] = str(firstName)

        else:
            self.set_status(406)             
            self.write(' first name is empty')
            return 


        lastName = self.get_argument('lastName','')
        if lastName !='':
            data['lastName'] = str(lastName)
        else:
            self.set_status(406)  
            self.write('empty last name')
            return 
        

        phone = str(self.get_argument('phone',''))
        
        if len(phone)== 10:
            data['phone'] = str(phone)
        else:
            self.set_status(406)  
            self.write('invalid phone number' )
            return 
         
                                        
        email = self.get_argument('email','')
        if email != '':
            data['email'] = str(email)
        else:
            self.set_status(406)  
            self.write('empty email')
            return 

        
        address = self.get_argument('address','')
        if address != '':
            data['address'] = str(address)
        else:
            self.set_status(406)  
            self.write('empty address')
            return 

        state = str(self.get_argument('state',''))
        if state != '':
            data['state'] = state
        else:
            self.set_status(406)  
            self.write('empty state')
            return 

        postal = str(self.get_argument('postal',''))
        if len(postal) == 5:
            data['postal'] = postal

        else:
            self.set_status(406)  
            self.write('invalid postal code')
            return 
        
                    
        #invoke data access
        uMgr =UserManagerFRS()
        
        #create new user node
        retVal = uMgr.createNewUserNode(data)

        #saved in success 0< else =0
        if retVal >0 :
            self.write(str(retVal))
            self.set_status(202)
        elif retVal == -1:
            self.set_status(409)
            self.write('-1')
        elif retVal == 0:
            self.set_status(417)
            self.write('417')
           

        


class BeforeCartAPI(tornado.web.Application):
    def __init__(self):
        handlers = [
            #FRS service handlers
                (r"/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/chatlist/?",SuggestFriendsForChatFRS),
                (r"/beforecart/frs/newfriends/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/savechat/?",saveNewChatFRS),
                (r"/beforecart/frs/createuser/?",CreateUserFRS)
            ]
        tornado.web.Application.__init__(self,handlers)





def main():

    app = BeforeCartAPI() #application
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
        
        main()