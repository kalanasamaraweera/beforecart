import os
import sys
import tornado
import pymongo
from tornado.options import  options
from tornado import ioloop, web

from Service import SuggestionHandlerPRS
from Service import UpdateHandlerPRS
from tornado.options import define

define("port", default=9915, help="port", type=int)
define("mongodb_host",default='localhost:27017', help='Monogo Database Host', type=str)
define("mongodb_name",default='Research', help='Database Name', type=str)
#define("user", default="root", help="tornado_api database user")
#define("password", default="", help="tornado_api database password")
define("init_db",default=1, help='Initisalize database', type=int)
define("static_path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','client'), help='static path', type=str)

#adding local directory to path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


'''
Connecting to the mongodb database
'''
mongo_client = pymongo.MongoClient(options.mongodb_host)
db = mongo_client[options.mongodb_name]

def init_db(db):
    try:
        db.create_collection('PRS')
    except:
        pass
    try:
        db['PRS'].insert({"id":0,"ready":"TRUE","suggestion_list":[1,2,3,4,5]}) # userId 0 is reserverd for the system.
    except:
        pass
    try:
        db['PRS'].update({'id':1}, {"$set":{"ready":"FALSE"}}, upsert=False)
    except:
        pass
    db['PRS'].ensure_index('id', unique=True)
    db['PRS'].ensure_index('_id', unique=True)

static_path = options.static_path

app = tornado.web.Application([(r'/api/suggestions', SuggestionHandler, dict(db=db)),(r'/api/updateSuggestions', UpdateHandler, dict(db=db))],
                        static_path=static_path,
                        autoreload=True
)

if __name__ == '__main__':
    #read settings from commandline
    options.parse_command_line()
    if options.init_db:
        init_db(db)
    print ('server running on http://localhost:{}'.format(options.port))
    app.listen(options.port,xheaders=True)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()