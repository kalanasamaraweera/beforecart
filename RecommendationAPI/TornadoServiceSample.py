import os
import sys
import tornado
import pymongo
from tornado.options import  options
from tornado import ioloop, web
from tornado.options import define
import json, traceback
from bson.objectid import ObjectId
#from indico.error import IndicoError, RouteNotFound, ServerError
#from indico.utils import LOGGER
from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import tornado.options
tornado.options.parse_command_line()
import logging


class JSONEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,ObjectId):
            return str(o)
        return json.JSONEncoder.default(self,o)


class MainHandler(tornado.web.RequestHandler):
     def get(self):
         self.write('Hello, World')
 
class UserHandler(tornado.web.RequestHandler) :
    def get(self):
        
        #logging.basicConfig(filename='notes.txt',level=logging.DEBUG)
        #logging.info(" Invoked suggest_new_pals_frs in")
        
        
        name = self.get_argument('name', 'Kalana')
        self.write('GET-Welcome '+str(name))   
    def post(self):
        #title= self.get_argument('title')
        json_data =json.loads(self.request.body)
        self.write('POST-Welcome'+str(json_data['book']))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/?",MainHandler),
                (r"/api/v1/users/?",UserHandler),
                (r"/api/v1/cars/[0-9][0-9][0-9][0-9]/?",UserHandler)
            ]
        tornado.web.Application.__init__(self,handlers)
    

def main():

    app = Application()
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
        main()
    


