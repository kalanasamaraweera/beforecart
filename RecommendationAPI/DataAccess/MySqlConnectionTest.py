import unittest
import  MySqlConnection
class Test_MySqlConnectionTest(unittest.TestCase):
    #def test_A(self):
    #    self.fail("Not implemented")

    def makeConnectionTest(self):
        connection = MySqlConnection()
        data=connection.makeConnection()
        if data =="":
            self.fail("makeConnectionTest failed")




if __name__ == '__main__':
    unittest.main()
