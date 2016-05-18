import tornado
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from slugify import slugify

class UpdateHandlerPRS(tornado.web.RequestHandler):
    def initialize(self, db):
        """
        Initializes the instance with a mongodn database instance
        :param db: an instance to pymongo database object
        """
        self._db = db

    def get(self):
        """
        Update suggestion list
        """
        userId = self.get_argument('id', None)
        status = self.get_argument('status', None)
        if userId and (status=='TRUE' or status=='FALSE'):
            record = list(self._db['PRS'].find({'id':int(userId)}))
            if len(record) > 0:
                print ('User ID          : %s' % userId)
                print ('User Status      : %s' % record[0]['ready'])
                if  record[0]['ready']=='TRUE' and status=='FALSE':
                    try:
                        self._db['PRS'].update({'id':int(userId)}, {"$set": {'ready':'FALSE'}}, upsert=False)
                        self.write(dumps({'status':'TRUE'}))
                    except Exception as e:
                        self.write(dumps({'status':'FALSE'}))
                elif record[0]['ready']=='FALSE' and status=='TRUE':
                    try:
                        self._db['PRS'].update({'id':int(userId)}, {"$set": {'ready':'TRUE'}}, upsert=False)
                        self.write(dumps({'status':'TRUE'}))
                    except Exception as e:
                        self.write(dumps({'status':'FALSE'}))
                else:
                    self.write(dumps({'status':'TRUE'}))
            else:
                print ('Not a valid user')
                self.write(dumps({'status':'FALSE'}))
        else:
            print ('Invalid request')
            self.write(dumps({'status':'FALSE'}))