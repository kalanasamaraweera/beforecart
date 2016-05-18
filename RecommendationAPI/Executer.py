from DataAccess import FriendshipBuilderFRS
from DataAccess import ChatHistoryFRS
from DataAccess import UserManagerFRS 
from DataAccess import DBConf
from datetime import timedelta as td
from datetime import datetime
import random

# delete all existing nodes and re-build network in databse server using AU-import2.csv
def buildUserNodesFRS():
    b = FriendshipBuilderFRS()
    b.buildInitUserNodesFromCsvFRS()



#delete existing friendship between two user nodes 
def breakExistingRelationshipServiceFRS(em1,em2):
    b =FriendshipBuilderFRS()
    return b.removeExistingRelationship(em1,em2)

#breakExistingRelationship()

#make new friendship between users
def makeNewRelationshipServiceFRS(em1,em2):
    b= FriendshipBuilderFRS()
    b.removeExistingRelationship(em1,em2)
    b.makeNewFriendship(em1,em2)
    
#Send friend request
def sendRequestServiceFRS(em1,em2):
    b = FriendshipBuilderFRS()
    return  b.sendFriendRequestFRS(em1,em2)

#Cancel friend request sent by sender
def cancelRequestBySenderServiceFRS(em1,em2):
    b =FriendshipBuilderFRS()
    return b.cancelFriendRequestFRS(em1,em2)



#Upgrade [:Requested] relationship to[:FRIEND_OF] 
def  acceptRequestServiceFRS(em1,em2):
    b =FriendshipBuilderFRS()
    return b.acceptNewFriendshipFRS(em1,em2)


#return all the friend nodes of User node
def getAllFriendsServiceFRS(em1):
    
     b= FriendshipBuilderFRS()
     return b.selectAllFriends(em1)

def getAllRequstsTowardUser(em1):
    b =FriendshipBuilderFRS()
    return b.getAllFriendRecievedRequests(em1)

def getAllSentRequestsByUser(em1):
    b =FriendshipBuilderFRS()
    return b.getAllPendingFriendRequests(em1) 

def checkFriendship(em1,em2):
    b = FriendshipBuilderFRS()
    return b.checkExistingFriendshipFRS(em1,em2)
 

def createNetworkFRS():
    b= FriendshipBuilderFRS()
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

def saveChat(email,friendList,conv):
    b = ChatHistoryFRS()
    print b.saveChatHistoryFRS(email,friendList,conv)

def getChats(uid):
    b = ChatHistoryFRS()
    print  b.getAllChatsOfUser(uid)


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
    b =FriendshipBuilderFRS()
    b.buildSingleUserNetwork()

def removeUser():
    b = UserManagerFRS()
    print b.removeUserNode("kalana@gmail.com")

def testConf():
    b =DBConf()
    print b.getNeoGraphConfig()

def upgrdeRel():
    b =FriendshipBuilderFRS()
    print b.upgradeRelationship('breana@yahoo.com','eveline@yahoo.com','strength',12)

def convertSampleChat():
    b = ChatHistoryFRS()
    b.convertSampleChat()

def saveChatData():
    b = ChatHistoryFRS()
    b.saveSampleChatData()

#changeProperty()
#saveChatData()

#buildSingleUserRels()
#changeProperty()
#testConf()
#saveUser()
#removeUser()
#upgrdeRel()
    

#friendlist=[{'1':'laurene_bennett@gmail.com','2':'stevie.hallo@hotmail.com'}]
#user=eml1
#conv =[{'1':'Whats Up','2':'Problem','3':'Tell Me','user':'Which is better?','4':'That one'}]
#saveChat(user,friendlist,conv)


#cus =getChats('rebbecca.didio@didio.com.au')
#print cus
def getRandomdate():
        b =FriendshipBuilderFRS()
        arr= b.getRandomDate()
        print arr[0]
        print arr[1]


getRandomdate()

#today = date.today()
#print "Today "+ str(today)
#oneday  = td(weeks=1)
#print "One Day "+str(oneday)
#yesterday =today -oneday
#print "Yesterday"+str(yesterday)
#tom = today + oneday
#print"Tommorow" +str(tom)



