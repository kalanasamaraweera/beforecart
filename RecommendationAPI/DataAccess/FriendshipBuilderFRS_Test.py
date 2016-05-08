import unittest
import FriendshipBuilderFRS

class Test_FriendshipBuilderFRS_Test(unittest.TestCase):
    #def test_A(self):
    #    self.fail("Not implemented")

    eml1="rebbecca.didio@didio.com.au"
    eml2="stevie.hallo@hotmail.com" 
    eml3="gerardo_woodka@hotmail.com"

    def removeExistingRelationship(self):
        b =FriendshipBuilderFRS()
        val =b.removeExistingRelationship(eml1,eml2)
        if val != True:
            self.fail("removeExistingRelationship Test Failed")
    



if __name__ == '__main__':
    unittest.main()
