import unittest
from DataAccess import SuggestionManagerFRS
class Test_SuggestionManagerTestFRS(unittest.TestCase):
    #def test_A(self):
    #    self.fail("Not implemented")

#Testing calculate scoreChatsNVotes()

    def scoreChatsNVotesTest(self):
        sMgr =  SuggestionManagerFRS()

        chats  = 700
        pvotes = 10
        nvotes = 12
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,100)



    



if __name__ == '__main__':
    unittest.main()
