import unittest

import UserManagerFRS 

class Test_UserManagerFRS(unittest.TestCase):
    def saveUser(self):
       data= {'username':'x','password':'x','email':'ss@f.c','phone':'2287632','postal':'23212','state':'Kandy','firstname':'f','lastname':'l','address':'x'}
       b = UserManagerFRS()
       sts=b.createNewUserNode(data)

       if sts==False:
           self.fail("createNewUserNode failed")

    def changeProperty(self):
        val ="kalana@gmail.com"
        prop = "email"
        email = 'ss@f.c'
        
        b =  UserManagerFRS()
        sts =  b.updateProperty(email,prop,val)
        print sts
        if sts !=False:
            self.fail("Update  did not happen")






if __name__ == '__main__':
    unittest.main()
    tm = Test_UserManagerFRS()
    tm.changeProperty()
