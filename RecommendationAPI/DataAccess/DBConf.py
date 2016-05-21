class DBConf(object):
   
    def __init__(self):
       DBConf =self
   
    def getNeo4jConfig(self):
       lines = [line.rstrip('\n') for line in open('NeoConf.txt')]
       elements =[]
       for element in lines:
           elements.append(element)
           
       return elements

    def getNeoGraphConfig(self):
       elements=self.getNeo4jConfig()
       return elements[3]


    def getMongoConf(self):
       lines = [line.rstrip('\n') for line in open('mongoConf.txt')]
       elements =[]
       for element in lines:
           elements.append(element)
           
       return elements

    def getMySqlConf(self):
       lines = [line.rstrip('\n') for line in open('MySqlConf.txt')]

