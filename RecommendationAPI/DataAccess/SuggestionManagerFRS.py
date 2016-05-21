#This class implements methods which measure friendship between two users and make appropriate suggestion lists of users
#to add in chat sessions and add as friends
#The friendship is measured based on no of interactions between users against time
#Therefore following class implements a scoring model to measure friend-ship between two user nodes
#Inorder to measure the friendship it uses
#   ~ No of chats between user
#   ~ Duration of relationships

from DataAccess import FriendshipManagerFRS
from DataAccess import UserManagerFRS

import operator
import json

class SuggestionManagerFRS(object):

    def __init__(self):
       SuggestionManagerFRS =self




    def makeFriendshipScore(self,email,friend):
      
      """ score friendship """
    # * the total score will be out of 100 %
    # * weight for chat frequencey is 60%
    # * weight for duration from last chat 40%

      friendMgr =FriendshipManagerFRS()

      array = friendMgr.selectRelationship(email,friend)
      
      c=0
      try:
          if len(array)==5:

                c+=1
                #print "\n Id:"+str(c)
                #print"User: %s"% str(i['email'])
                #print "Dur:%s days from last chat" % str(i['duration'])
                #print "Chats: %s chats"% str(i['chats'])
                total=-1
                chatVoteScore=self.scoreChatsNVotes(array[0],array[2],array[3])
                durationScore=self.scoreDur(array[1])
                total =self.calculateTotalScore(chatVoteScore,durationScore)
                #deduct / add  by votes

                #print "chat score %s"% str(chatScore)
                #print "duration score %s" % str(durationScore)
                #print "total score %s"%str(float(total)/float(100))

                "return score"
                return float(total)/100.0
    
      except Exception, e:
          print str(e.message)

              

              

    
    def scoreChatsNVotes(self,chats,pvotes,nvotes):
        "Score Chats represents the affnity score"
        # 0 : 0
        # >250 : 60
        # 0-25 : 10
        #25-50 : 20
        #50-100 :30
        #100-150:40
        #150-250:50
         
        chats =int(chats)
        pvotes= int(pvotes)
        nvotes = int(nvotes)

        if chats == 0:  #no chats  no marks
            if pvotes>nvotes:#if pvotes>=nvotes socre:+5 only ;else return 0
                return 5
            else:return 0

        if 250<chats:   # chats more than 250  full marks
            if nvotes>pvotes :#chats ?votes-5only
                return  55
            else:return 60
            
        score=0
        if  0<chats and chats <= 25: 
            score= 10
        elif 25<chats and chats<=50:
            score= 20
        elif  chats<50 and chats<=150:
            score= 30
        elif 150<chats and chats<=250:
            score= 40
        score=self.voteHandler(score,pvotes,nvotes)
        return score


    #score for votes
    def voteHandler(self,score,pv,nv):

        pv =int(pv)
        nv= int(nv)

        if score>=5:
        
            if pv>= nv:
                score+=5
            elif pv<nv:
                score-=5
        return score

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


    #calculate cumulative score
    def calculateTotalScore(self,chat,duration):

        if chat!=None and duration != None:
            return chat+ duration
        else:
            if chat ==None:
                chat =0
            if duration  == None:
                duration = 0
            return duration + chat

    
    #sort Decending expertise in 8 product categories
    def sortUserPreferences(self,user):

        userMgr =UserManagerFRS()
        categories = userMgr.getCategoryExp(user)
        
        #sort list
        if len(categories)!=0:
            categories=sorted(categories.items(), key=operator.itemgetter(1))
        
        return categories


    #get maximum category out of  given list of  product categories
    def getMaxCategory(self,categories):

        
        categories = dict(categories)
        
        maxIndex=max(categories.items(), key=operator.itemgetter(1))[0] # index of max.
        maxValue =max(categories.items(), key=operator.itemgetter(1))[1] # max. value
        
        maxCat ={maxIndex:maxValue}
        return maxCat


     #prepare list of users for chat on product
    def makeChatSuggestionList(self,user,category):

        freindMgr = FriendshipManagerFRS()
        userMgr = UserManagerFRS()

        allFriends = freindMgr.selectAllFriends(user)

        for friend in allFriends:

            email = friend['email']
    
            
    #update all the relationship strength of user
    def upgradeRelationshipStrength(self,user):

        fMgr = FriendshipManagerFRS()
        user =str(user)
        allFriends = fMgr.selectAllFriends(user)
        
        for friend in allFriends:
            score=0
            try:
                email = str(friend['email'])
                score =self.makeFriendshipScore(user,email) #calculate friendship score
                fMgr.upgradeRelationship(user,email,"strength",score)
                    
            except Exception,e:
                print str(e.message)+" -2"
                continue
            finally:print email+"-> STR:"+str(score)

    
    #refine selected list of users for chat
    def refineChatList(self,user,category):

        friendMgr = FriendshipManagerFRS()
        uMgr =UserManagerFRS()
        expFriends = friendMgr.selectFriendsForChatOnExp(user,category)
        closeFriends = friendMgr.selectAllFriends(user)

        #print expFriends 

        mixList=self.mixLists(closeFriends,expFriends)
        
        for i in  mixList:
           item =str(i)
           print item +" count "+str(mixList.count(item))

        return mixList


    def mixLists(self,closeFriends,expFriends):

        finalList=[]

        for OutItem in closeFriends:
            chk =finalList.count(OutItem['email'])
            if chk==0:
                finalList.append(OutItem['email'])
            else:continue

            for InItem  in expFriends:
                    chkIn =finalList.count(InItem['email'])
                    if chkIn ==0:
                        if OutItem!=InItem:
                            finalList.append(InItem['email'])
                            break

                    else:continue

        return finalList
            

                 







        
    
   
    
        
        














        


        



        









    

 


