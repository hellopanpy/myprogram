# --*--coding:utf8--*--

'''
collect mongodb quota
'''
__version__ = '1.0'
__author__ = 'panpy'

import pymongo
import re
from time import sleep
from optparse import OptionParser

class Monit_mongo:

    def __init__(self,mongo_uri,timeout=3):

        self.mongo_uri = mongo_uri
        self.timeout = timeout

    def get_dict(self):

        try:
            self.mongo_cli = pymongo.mongo_client.MongoClient(
                self.mongo_uri,
                socketTimeoutMS=self.timeout,
                read_preference=pymongo.ReadPreference.PRIMARY_PREFERRED)
            db = self.mongo_cli['admin']
            result = db.command('serverStatus')
            self.mongo_cli.close()
            return result

        except Exception:
            raise

    def get_value(self,model,key):
        dict = self.get_dict()
        if not re.match('.*?\..*',key):
            value = dict[model][key]
            print value
        else:
            key_list = key.split('.')
            value = dict[model][key_list[0]][key_list[1]]
            print value
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--uri", type="string", help="uri", dest="uri", action="store")
    parser.add_option("-m", "--model", type="string", help="model", dest="model", action="store")
    parser.add_option("-k", "--key", type="string", help="key", dest="key", action="store")
    (options, args) = parser.parse_args()
    if options.uri:
        mongo_cli = Monit_mongo(options.uri)
        if options.model and options.key:
            mongo_cli.get_value(options.model, options.key)
        else:
            print "Invalid input!"
    else:
        print "No input uri!"

