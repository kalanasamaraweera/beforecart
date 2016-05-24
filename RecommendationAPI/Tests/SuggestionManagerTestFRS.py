import unittest
from DataAccess import SuggestionManagerFRS
class Test_SuggestionManagerTestFRS(unittest.TestCase):
    #Testing calculate scoreChatsNVotes()

    def test_A(self):

        sMgr =  SuggestionManagerFRS()
        chats  = 700
        pvotes = 10
        nvotes = 12
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,55)
    
    def test_B(self):

        sMgr =  SuggestionManagerFRS()
        chats  = 0
        pvotes = 40
        nvotes = 12
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,5)

    def test_C(self):

        sMgr =  SuggestionManagerFRS()
        chats  = 12
        pvotes = 0
        nvotes = 0
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,10)
    
    def test_D(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 30
        pvotes = 0
        nvotes = 0
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,20)

    def test_E(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 70
        pvotes = 0
        nvotes = 0
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,30)

    def test_E(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 170
        pvotes = 0
        nvotes = 0
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,40)

    def test_F(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 270
        pvotes = 0
        nvotes = 0
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,50)  
         
    def test_G(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 600
        pvotes = 10
        nvotes = 9
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,60) 

    def test_H(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 0
        pvotes = 10
        nvotes = 29
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,0)
         
    def test_I(self):
        sMgr =  SuggestionManagerFRS()
        chats  = 700
        pvotes = 10
        nvotes = 29
        result = sMgr.scoreChatsNVotes(chats,pvotes,nvotes)
        self.assertEqual(result,55) 


#Test scoreDur( duration)

    def test_J(self):
        sMgr =  SuggestionManagerFRS()
        dur = 0
        result = sMgr.scoreDur(dur)
        self.assertEqual(result,40)
 
    def test_K(self):
        sMgr =  SuggestionManagerFRS()
        dur = 735
        result = sMgr.scoreDur(dur)
        self.assertEqual(result,0) 
            
    def test_L(self):
        sMgr =  SuggestionManagerFRS()
        dur = 150
        result = sMgr.scoreDur(dur)
        self.assertEqual(result,30)

    def test_M(self):
        sMgr =  SuggestionManagerFRS()
        dur = 184
        result = sMgr.scoreDur(dur)
        self.assertEqual(result,20) 
                
    def test_N(self):
        sMgr =  SuggestionManagerFRS()
        dur = 370
        result = sMgr.scoreDur(dur)
        self.assertEqual(result,10)

 # test voteHandler(self,score,pv,nv)       
    
    def test_O(self):
        sMgr =SuggestionManagerFRS()
        score  =0
        pv=7
        nv =5
        result = sMgr.voteHandler(score,pv,nv)
        self.assertEqual(result,0)

    def test_P(self):
        sMgr =SuggestionManagerFRS()
        score  =5
        pv=7
        nv =5
        result = sMgr.voteHandler(score,pv,nv)
        self.assertEqual(result,10)

    def test_Q(self):
        sMgr =SuggestionManagerFRS()
        score =5
        pv=2
        nv =5
        result = sMgr.voteHandler(score,pv,nv)
        self.assertEqual(result,0)

    def test_R(self):
        sMgr =SuggestionManagerFRS()
        score  =25
        pv=2
        nv =5
        result = sMgr.voteHandler(score,pv,nv)
        self.assertEqual(result,20)

if __name__ == '__main__':
    unittest.main()
