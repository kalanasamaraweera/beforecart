from DataAccess import FriendshipBuilderFRS 

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