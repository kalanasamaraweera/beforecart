import tornado
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from slugify import slugify
from DataAccess import RequestHandlerPRS

class SuggestionHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        """
        Initializes the instance with a mongodn database instance
        :param db: an instance to pymongo database object
        """
        self._db = db

    def get(self):
        """
        Returns suggestion list
        """
        userId = self.get_argument('id', None)
        count = self.get_argument('count', None)
        if userId and count:
            record = list(self._db['PRS'].find({'id':int(userId)}))
            if len(record) > 0:
                print ('User ID          : %s' % userId)
                print ('Suggestion count : %s' % count)
                print ('User Status      : %s' % record[0]['ready'])
                print ('User suggestions : %s' % record[0]['suggestion_list'])
                if  record[0]['ready']=='TRUE' and len(record[0]['suggestion_list'])>=int(count):
                    self.write(dumps({'status':'TRUE','suggestion_list':record[0]['suggestion_list'][:int(count)]}))
                else:
                    print ('Generate suggestions')
                    suggestions = DataAccess.getSuggestionListPRS(0,int(count))
                    try:
                        print (suggestions)
                        self._db['PRS'].update({'id':int(userId)}, {"$set": {'ready':'TRUE','suggestion_list':suggestions}}, upsert=False)
                        self.write(dumps({'status':'TRUE','suggestion_list':suggestions}))
                    except Exception as e:
                        print ('Update Failed')
                        self.write(dumps({'status':'FALSE'}))
            else:
                print ('Not a valid user')
                self.write(dumps({'status':'FALSE'}))
        else:
            print ('Invalid request')
            self.write(dumps({'status':'FALSE'}))
#rdgdgdgfdgfgdggdgfdgdgfdgdgfdgdgdfgd
    #def post(self):
    #    """
    #    add a new blog
        
    #    """
    #    blog = loads(self.request.body.decode("utf-8"))
    #    if not blog['name']:
    #        self.write(dumps({'status':-1,'error':'name is mandatory'}))
    #        return
    #    #create a slug for the blog
    #    slug = slugify(blog['name'])
    #    #make sure slug in unique in blog collection
    #    # the following request will return all slug in the collection
    #    blog_slugs = self._db['blog'].distinct('slug')

    #    nslug = slug
    #    i=0
    #    while nslug in blog_slugs:
    #        nslug = '{}-{}'.format(slug, i)
    #        i+=1
    #    blog['slug']=nslug
    #    try:
    #        self._db['blog'].insert(blog)
    #        self.write({'status':0,'error':'','slug':blog['slug']})
    #    except Exception as e:
    #        self.write(dumps({'status':-2,'error':str(e)}))

    #def put(self):
    #    """
    #    updates an existing blog
        
    #    """
    #    blog = loads(self.request.body.decode("utf-8"))
    #    try:
    #        ret = self._db['blog'].update({'_id':ObjectId(blog['_id'])}, {"$set": blog}, upsert=False)
    #        self.write(dumps(ret))
    #    except Exception as e:
    #        self.write(dumps({'status':'error','error':str(e)}))

    #def delete(self):
    #    """
    #    delete a blog
    #    """
    #    _id = self.get_argument('_id', False)
    #    try:
    #        ret = self.db['blog'].remove({'_id':ObjectId(_id)})
    #        self.write(dumps(ret))
    #    except Exception as e:
    #        self.write(dumps({'status':'error','error':str(e)}))
