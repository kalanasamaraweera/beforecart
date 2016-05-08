from DataAccess import FriendshipBuilderFRS 

# delete all existing nodes and re-build network in databse server using AU-import2.csv
def buildNetworkOfFriendsFRS():
    b = FriendshipBuilderFRS()
    b.fillUserNodesFromCsvFRS()



#delete existing friendship between two user nodes 
def breakExistingRelationship(em1,em2):
    b =FriendshipBuilderFRS()
    b.removeExistingRelationship(em1,em2)

#breakExistingRelationship()

#make new friendship between users
def makeNewRelationshipServiceFRS(em1,em2):
    b= FriendshipBuilderFRS()
    b.removeExistingRelationship(em1,em2)
    b.makeNewFriendship(em1,em2)
    

def sendRequestServiceFRS(em1,em2):
    b = FriendshipBuilderFRS()
    b.sendFriendRequestFRS(em1,em2)

#Cancel friend request sent by sender
def cancelRequestBySenderServiceFRS(em1,em2):
    b =FriendshipBuilderFRS()
    b.cancelFriendRequestBySenderFRS(em1,em2)

#Reject request by reciver
def cancelRequestByReciverServiceFRS(em1,em2):
    b =FriendshipBuilderFRS()
    b.cancelRequestByRecieverFRS(em1,em2)

#Upgrade [:Requested] relationship to[:FRIEND_OF] 
def  acceptRequestServiceFRS(em1,em2):
    b =FriendshipBuilderFRS()
    b.acceptNewFriendshipFRS(em1,em2)


#return all the friend nodes of User node
def getAllFriendsServiceFRS(em1):
    
     b= FriendshipBuilderFRS()
     b.selectAllFriends(em1)

def checkFriendship(em1,em2):
    b = FriendshipBuilderFRS()
    return b.checkExistingFriendshipFRS(em1,em2)
       

eml1="rebbecca.didio@didio.com.au"
eml2="stevie.hallo@hotmail.com" 
eml3="gerardo_woodka@hotmail.com"

x= checkFriendship(eml1,eml3)
print  x
#sendRequestServiceFRS(eml1,eml2)
#cancelRequestBySenderServiceFRS(eml2,eml1)
#cancelRequestByReciverServiceFRS(eml2,eml1)
#acceptRequestServiceFRS(em1,em2)
#breakExistingRelationshipServiceFRS(eml2,eml1)
#getAllFriendsServiceFRS(eml2)
#getAllFriendsServiceFRS(eml1)
#makeNewRelationshipFRSServiceFRS(eml3,eml1)
#buildNetworkOfFriendsFRS()