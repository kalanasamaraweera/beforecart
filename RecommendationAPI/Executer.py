from DataAccess import FriendshipManagerFRS
from DataAccess import SuggestionManagerFRS
from DataAccess import ChatHistoryFRS
from DataAccess import UserManagerFRS 
from DataAccess import DBConf
from datetime import timedelta as td
from datetime import datetime


import random
import json

# delete all existing nodes and re-build network in databse server using AU-import2.csv
def buildUserNodesFRS():
    b = FriendshipManagerFRS()
    b.buildInitUserNodesFromCsvFRS()



#delete existing friendship between two user nodes 
def breakExistingRelationshipServiceFRS(em1,em2):
    b =FriendshipManagerFRS()
    return b.removeExistingRelationship(em1,em2)

#breakExistingRelationship()

#make new friendship between users
def makeNewRelationshipServiceFRS(em1,em2):
    b= FriendshipManagerFRS()
    b.removeExistingRelationship(em1,em2)
    b.makeNewFriendship(em1,em2)
    
#Send friend request
def sendRequestServiceFRS(em1,em2):
    b = FriendshipManagerFRS()
    return  b.sendFriendRequestFRS(em1,em2)

#Cancel friend request sent by sender
def cancelRequestBySenderServiceFRS(em1,em2):
    b =FriendshipManagerFRS()
    return b.cancelFriendRequestFRS(em1,em2)



#Upgrade [:Requested] relationship to[:FRIEND_OF] 
def  acceptRequestServiceFRS(em1,em2):
    b =FriendshipManagerFRS()
    return b.acceptNewFriendshipFRS(em1,em2)


#return all the friend nodes of User node
def getAllFriendsServiceFRS(em1):
    
     b= FriendshipManagerFRS()
     return b.selectAllFriends(em1)

def getAllRequstsTowardUser(em1):
    b =FriendshipManagerFRS()
    return b.getAllFriendRecievedRequests(em1)

def getAllSentRequestsByUser(em1):
    b =FriendshipManagerFRS()
    return b.getAllPendingFriendRequests(em1) 

def checkFriendship(em1,em2):
    b = FriendshipManagerFRS()
    return b.checkExistingFriendshipFRS(em1,em2)
 

def createNetworkFRS():
    b= FriendshipManagerFRS()
    b.buildInitFriendsNetworkFRS()      

eml1="rebbecca.didio@didio.com.au"
eml2="stevie.hallo@hotmail.com" 
eml3="laurene_bennett@gmail.com"


#print sendRequestServiceFRS(eml1,eml3)
#print getAllRequstsTowardUser(eml1)
#print getAllSentRequestsByUser(eml2)
#print cancelRequestBySenderServiceFRS(eml1,eml2)

#print acceptRequestServiceFRS(eml1,eml3)
#print breakExistingRelationshipServiceFRS(eml1,eml3)
#print getAllFriendsServiceFRS(eml1)

#makeNewRelationshipFRSServiceFRS(eml3,eml1)
#buildNetworkOfFriendsFRS()
#createNetworkFRS()
#buildUserNodesFRS()

#ChatHistoryFRS--------

def saveChat():
    friendlist={'1':'rebbecca.didio@didio.com.au','2':'stevie.hallo@hotmail.com'}
    user="kalana331@gmail.com"
    conv =[{'1':'Whats Up','2':'Problem','3':'Tell Me','user':'Which is better?','4':'That one'}]
    b = ChatHistoryFRS()
    conv=str(json.dumps(conv))
    b.saveChatHistoryFRS(user,friendlist,conv)

def getChats(uid):
    b = ChatHistoryFRS()
    chats=  b.getAllChatsOfUser(uid)
    cont=0
    for chat in chats:
        cont+=1
        print "\n"+str(cont)
        print chat['friend']
        print chat['time']



def saveUser():
    data= {'username':'kalana','password':'kalana','email':'kalana@gmail.com','phone':'0728419199','postal':'22342','state':'Colombo','firstname':'Kalana','lastname':'Samaraweera','address':'Gampaha'}
    b = UserManagerFRS()
    print b.createNewUserNode(data)

def getUserId(email):
    b = UserManagerFRS()
    return b.getUserId(email)

#print getUserId('ss@f.c')
def changeProperty():

    prop = "cat"
    email = 'kalana331@gmail.com'
        
    b =  UserManagerFRS()
    sts =  b.updateProperty(email,prop+str(1),0.23434)
    print sts


def buildSingleUserRels():
    b =FriendshipManagerFRS()
    b.buildSingleUserNetwork()

def removeUser():
    b = UserManagerFRS()
    print b.removeUserNode("kalana@gmail.com")

def testConf():
    b =DBConf()
    print b.getNeoGraphConfig()

def upgrdeRel():
    b =FriendshipManagerFRS()
    print b.upgradeRelationship('breana@yahoo.com','eveline@yahoo.com','strength',12)

def convertSampleChat():
    b = ChatHistoryFRS()
    b.convertSampleChat()

def saveChatData():
    b = ChatHistoryFRS()
    b.saveSampleChatData()

def increaseChats():
    b =FriendshipManagerFRS()
    b.increaseChatCount("kalana331@gmail.com","idella@hotmail.com")


def increaseDuration():
    b =FriendshipManagerFRS()
    b.increaseDuration("kalana331@gmail.com")

#def saveChat():
#    friends =["idella@hotmail.com","stevie.hallo@hotmail.com"]
#    chatlist =[]
#    chatlist.append({"stevie":"whats the best shirt"})
#    chatlist.append({"me":"blue one"})
#    b =ChatHistoryFRS()
#    b.saveChatHistoryFRS("kalana331@gmail.com",friends,chatlist)

def changePVotes():
    b =FriendshipManagerFRS()
    user="kalana331@gmail.com"
    friend ="rebbecca.didio@didio.com.au"
    print b.changePosVotes(user,friend,'-')

def strenUpdate():
        m =SuggestionManagerFRS()
        m.upgradeRelationshipStrength("kalana331@gmail.com")


def refineChatList():
    user="kalana331@gmail.com"
    cat="cat1"
    f =SuggestionManagerFRS()
    f.refineChatList(user,cat)

def buildFriendsOfFriendNetwork():
     f =SuggestionManagerFRS()
     f.buildFriendsOfFriendNetwork()

buildFriendsOfFriendNetwork()

def destructFriendOfFriendNetwork():
    f=SuggestionManagerFRS()
    f.destructFriendOfFriendNetwork()

#destructFriendOfFriendNetwork()

#changePVotes()
#increaseChats()
#saveChat()
#increaseDuration()
#changeProperty()
#saveChatData()

#buildSingleUserRels()
#changeProperty()
#testConf()
#saveUser()
#removeUser()
#upgrdeRel()
    


#saveChat()


#getChats('kalana331@gmail.com')


#def getRandomdate():
#        b =FriendshipManagerFRS()
#        arr= b.getRandomDate()
#        print arr[0]
#        print arr[1]


#getRandomdate()

#today = date.today()
#print "Today "+ str(today)
#oneday  = td(weeks=1)
#print "One Day "+str(oneday)
#yesterday =today -oneday
#print "Yesterday"+str(yesterday)
#tom = today + oneday
#print"Tommorow" +str(tom)

def getex():
    b =FriendshipManagerFRS()
    arr =b.selectExpertiseOfFriends("kalana331@gmail.com","cat1")

    arr= json.loads(arr)
    for i in arr:
        print i['exp']

#def score():
#     s =SuggestionManagerFRS()
#     s.makeFriendshipScore("kalana331@gmail.com")

#score()

