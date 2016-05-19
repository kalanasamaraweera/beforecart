#This class implements methods which measure friendship between two users.
#The friendship is measured based on no of interactions between users against time
#Therefore following class implements a scoring model to measure friend-ship between two user nodes
#Inorder to measure the friendship it uses
#   ~ No of chats between user
#   ~ Duration of relationships

 # 1.get all the friends of user from remote database

from DataAccess import FriendshipManagerFRS
from DataAccess import UserManagerFRS

import json

class SuggestionManagerFRS(object):

    def __init__(self):
       SuggestionManagerFRS =self

   # get friends 
    #def suggestFriendsForChat(self,email,category):
        
    #    userMgr =  UserManagerFRS.UserManagerFRS()
    #    friendMgr =FriendshipManagerFRS.FriendshipManagerFRS()
    #    results = friendMgr.selectExpertiseOfFriends(email,category)
    #    arr =json.loads(results)

    #    if  arr[0]!=0:


    def makeFriendshipScore(self,email):
      
      """ score friendship """
    # * the total score will be out of 100 %
    # * weight for chat frequencey is 60%
    # * weight for duration from last chat 40%

      friendMgr =FriendshipManagerFRS()

      array = friendMgr.selectAllFriends(email)
      array =json.loads(array)
      c=0
      if array!=0:
          for i in array:
              c+=1
              print "\n Id:"+str(c)
              print"User: %s"% str(i['email'])
              print "Dur:%s days from last chat" % str(i['duration'])
              print "Chats: %s chats"% str(i['chats'])

              noOfChats  = i['chats']
              duration = i['duration']
              user = i['email']
              




              chatScore=self.scoreChats(noOfChats)
              durationScore=self.scoreDur(duration)
             
              total =self.calculateTotalScore(chatScore,durationScore)

              print "chat score %s"% str(chatScore)
              print "duration score %s" % str(durationScore)
              print "total score %s"%str(float(total)/float(100))
              

              

    
    def scoreChats(self,chats):
        "Score Chats represents the affnity score"
        # 0 : 0
        # >250 : 60
        # 0-25 : 10
        #25-50 : 20
        #50-100 :30
        #100-150:40
        #150-250:50
         
        chats =int(chats)

        if chats == 0:  #no chats
            return 0

        if 250<chats:   #more than 250 chats
            return 60

        if  0<chats and chats <= 25:
            return 10
        elif 25<chats and chats<=50:
            return 20
        elif  chats<50 and chats<=150:
            return 30
        elif 150<chats and chats<=250:
            return 40


   #score Duration
    def scoreDur(self,dur):
        "duration represents time decay"
        dur =int(dur)

        if 730 <dur:        #more than 2 years
            return 0

        if dur ==0:         # today
            return 40

        if 0<dur and  dur<=182: #less than 6 months
            return 30
        elif 182<dur and 365>=dur: # 6 month - 1 year
            return 20
        elif 365<dur and 730>=dur:# 1 year - 2 years
            return 10


    def calculateTotalScore(self,chat,duration):

        if chat!=None and duration != None:
            return chat+ duration
        else:
            if chat ==None:
                chat =0
            if duration  == None:
                duration = 0
            return duration+chat








        


        



        









    

 


