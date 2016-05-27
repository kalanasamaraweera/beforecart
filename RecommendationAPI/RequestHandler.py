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
            
           # print (" Invoked suggest_new_pals_frs in FriendshipHandlerFRS.py \n TIME :"+ str(datetime.datetime.today())+"\n Returned:\n")
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
            self.write('400') 

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
               self.write('404')                    
            
        else:
            print ("Invalid userID or catId ;\n userId:"+str(userId))
            self.set_status(406)
            self.write('406')


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
                        self.write('417')
                else:
                    print 'Could not find matching email address .Chat did not saved in server userId'+str(userId)+" on,"+str(datetime.datetime.today())
                    self.write('404')
            else:
                print 'invalid data given for userId'+str(userId)+",on "+str(datetime.datetime.today())
                self.write_error(203)
    
    #get method
    def get(self):
        print ('get method is not supported')
        self.write_error(501)

class CreateUserFRS(tornado.web.RequestHandler):
    #create new user
    def post(self):
        
        #declare user data  dictionary
        data ={}

        #dispatch request data into dictionary
        username = self.get_argument('username','')
        data['username'] = str(username)
      
        password = self.get_argument('password','')
        data['password'] = str(password)
        
        firstName = self.get_argument('firstName','')
        data['firstName'] = str(firstName)

        lastName = self.get_argument('lastName','')
        data['lastName'] = str(lastName)
      
        phone = str(self.get_argument('phone',''))
        data['phone'] = str(phone)
                                       
        email = self.get_argument('email','')
        data['email'] = str(email)

        address = str(self.get_argument('address',''))
        data['address'] = str(address)
       
        state = str(self.get_argument('state',''))
        data['state'] = state
      
        postal = str(self.get_argument('postal',''))
        data['postal'] = postal

        #invoke data access
        uMgr =UserManagerFRS()

        #validate data in dictionary
        isValid = uMgr.validateUserData(data)

        #if userdata is valid
        if isValid == True:
            
            #create new user node
            retVal = uMgr.createNewUserNode(data)

            #saved in success 0< return new user id
            if retVal >0 :
                self.write(str(retVal))
                self.set_status(201)

            # already an  user exists for given email
            elif retVal == -1:  
                self.set_status(409)
                self.write('-1')

            #exception in data access
            elif retVal == 0:
                self.set_status(417)
                self.write('0')
                
        else: #validation failed
            self.write('0')
                   
      
        
class SendFriendRequest(tornado.web.RequestHandler):

    # send friendship request to an user
     def get(self):
             
         uMgr = UserManagerFRS()
         fMgr = FriendshipManagerFRS()
         isMade =False #relationship status 

         #filter  user ids from client request
         actionUserId = str(self.get_argument('userId','0')) #action user
         targetUserId = str(self.get_argument('friendId','0')) #tagert user
         
         #if user ids are valid >0
         if int(actionUserId) != 0 and int(targetUserId) !=0 and int(actionUserId) != int(targetUserId):
         
             #get user emails   
             aEmail = str(uMgr.getUserEmail(actionUserId)) #action user email
             tEmail = str(uMgr.getUserEmail(targetUserId) )#targeted user email

             #if emails are not empty 
             if aEmail != '' and tEmail != '':
                 
                 # make friendship request
                 isMade = fMgr.sendFriendRequestFRS(aEmail,tEmail)

                 #if friend request made
                 if isMade==True:
                     #accepted
                    self.set_status(202) 
                    self.write('200')

                 else: 
                     #exception occured   
                    self.set_status(417) 
                    self.write('417')   
                              
             else:#either one email is/are empty
                self.set_status(404) 
                self.write('404')            

         else: #invalid user ids
            self.set_status(404)
            self.write('404')
       
#return all sent and pending friend requests by user
class AllPendingRequests(tornado.web.RequestHandler):

    def get(self):

        #filter user id from request
        userId = str(self.get_argument('userId','0'))

        #check userId is in request
        if int(userId)>0:
            
            #create UserManager object
            uMgr = UserManagerFRS()
            fMgr = FriendshipManagerFRS()

            #get email of user
            email = uMgr.getUserEmail(userId)
            if email != '':
                #get all pending request
                response = str(fMgr.getAllPendingFriendRequests(email))
                self.write(response)
            else:
                #email not found
                self.write(404)
                self.write('')

        else:
            #bad request
            self.set_status(400)
            self.write('') 

#return all recieved requests
class AllRecievedRequests(tornado.web.RequestHandler):
    
        def get(self):

            #get user id from request
            userId = str(self.get_argument('userId','0'))
            
            #check user id is valid >0
            if int(userId) > 0:

                #invoke Data Access
                uMgr =UserManagerFRS()
                fMgr =FriendshipManagerFRS()

                #get email 
                email = uMgr.getUserEmail(userId)
                
                # if validate email not empty
                if email != '':
                        #get request list
                    requestSet =str( fMgr.getAllFriendRecievedRequests(email))
                    self.write(requestSet)

                else:
                    #bad request
                    self.set_status(400) 
                    self.write('')

            #user id invalid
            else:
                #bad request
                self.set_status(400)
                self.write('')
                 

#accept a recieved  friend request
class AcceptFriendRequest(tornado.web.RequestHandler):

    def get(self):

        # filter userId and friendId
        userId = str(self.get_argument('userId','0'))
        friendId = str(self.get_argument('friendId','0'))

        #check ids are empty
        if userId !='0' and friendId !='0':

            #invoke data access
            uMgr =UserManagerFRS()

            #get emails
            userEmail = uMgr.getUserEmail(userId)
            friendEmail = uMgr.getUserEmail(friendId)

            #check emails
            if userEmail !='' and friendEmail != '':

                #create FriendMgr. object
                fMgr = FriendshipManagerFRS()

                #build new friendship ; friend-sender, user-reciver
                status = fMgr.acceptNewFriendshipFRS(friendEmail,userEmail)

                #build new friend relationship
                if status == True:
                    self.set_status(200)
                    self.write('200')

                else:
                    #exception failed
                    self.set_status(417) 
                    self.write('417')

            else:#no emails
                self.set_status(404)
                self.write('404')

        else:#no user ids
            self.set_status(404)
            self.write('404')


#Reject friend request 
class RejectFriendRequest(tornado.web.RequestHandler):
    
    def get(self):

        # filter userId and friendId
        userId = str(self.get_argument('userId','0'))
        friendId = str(self.get_argument('friendId','0'))

        #check ids are empty
        if userId !='0' and friendId !='0':

            #invoke data access
            uMgr =UserManagerFRS()

            #get emails
            userEmail = uMgr.getUserEmail(userId)
            friendEmail = uMgr.getUserEmail(friendId)

            #check emails
            if userEmail !='' and friendEmail != '':

                #create FriendMgr. object
                fMgr = FriendshipManagerFRS()

                #remove existing relation request
                status = fMgr.cancelFriendRequestFRS(friendEmail,userEmail)

                #build new friend relationship
                if status == True:
                    self.set_status(200)
                    self.write('200')

                else:
                    #exception failed
                    self.set_status(417) 
                    self.write('417')

            else:#no emails
                self.set_status(404)
                self.write('404')

        else:#no user ids
            self.set_status(404)
            self.write('404')

 




#return all friends of user 
class AllFriendsOfUser(tornado.web.RequestHandler):
    
    def get(self):

            #get user id from request
            userId = str(self.get_argument('userId','0'))
            
            #check user id is valid >0
            if int(userId) > 0:

                #invoke Data Access
                uMgr =UserManagerFRS()
                fMgr =FriendshipManagerFRS()

                #get email 
                email = uMgr.getUserEmail(userId)
                
                # if validate email not empty
                if email != '':
                    
                    #get request list
                    requestSet = str(json.dumps(fMgr.selectAllFriends(email)))
                    self.write(requestSet)


                else:
                    #bad request
                    self.set_status(400) 
                    self.write('')

            #user id invalid
            else:
                #bad request
                self.set_status(400)
                self.write('') 


#Search Friends/Users
class FindUserRequest(tornado.web.RequestHandler):
    
    def get(self):
    
        #filter user id
        key = str(self.get_argument('key',''))
        userId =str(self.get_argument('userId','0'))
        
        #if key id  is not empty
        if key != '' and int(userId) >0:
            
            #invoke data access
            uMgr = UserManagerFRS()
            results = uMgr.searchUser(str(key),userId)

            if results !='0':
            #convert results to json
                 results =json.dumps(results)
                 self.write(results)
            else:
                self.write('')

            

        else:
           self.set_status(417)
           self.write('')




class BeforeCartAPI(tornado.web.Application):
    def __init__(self):
        handlers = [
            #FRS service handlers
                (r"/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/chatlist/?",SuggestFriendsForChatFRS),
                (r"/beforecart/frs/newfriends/?",SuggestNewFriendsFRS),
                (r"/beforecart/frs/savechat/?",saveNewChatFRS),
                (r"/beforecart/frs/createuser/?",CreateUserFRS),
                (r"/beforecart/frs/sendrequest/?",SendFriendRequest),
                (r"/beforecart/frs/sentrequests/?",AllPendingRequests),
                (r"/beforecart/frs/recievedrequests/?",AllRecievedRequests),
                (r"/beforecart/frs/allfriends/?",AllFriendsOfUser),
                (r"/beforecart/frs/acceptrequest/?",AcceptFriendRequest),
                (r"/beforecart/frs/rejectrequest/?",RejectFriendRequest),
                (r"/beforecart/frs/finduser/?",FindUserRequest)                
            ]
        tornado.web.Application.__init__(self,handlers)





def main():

    app = BeforeCartAPI() #application
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
        
        main()