import pymongo
import base64
import bson
from bson.binary import Binary
from urlparse import urlparse
import hashlib


class dbConn:
    dbname = "testdb"
    def __init__(self):
        self.__operation=None

    def operation(self, operation):
        self.set_operation(operation)
        if self.get_operation() == 'signup' or self.get_operation() == 'login':
            self.set_collection("users")
        elif self.get_operation() == "insert_image":
                self.set_collection('fileCollections')

    def get_operation(self):
        return self.__operation
    def set_operation(self,operation):
        self.__operation=operation
    def get_collection(self):
        return self.__collection
    def set_collection(self,collection):
        self.__collection=collection

    def establishConnection(self):
        # establish a connection to the database
        uri = "mongodb://admin:admin@127.0.0.1:27017"
        try:
            client = pymongo.MongoClient(uri)
            print("succesfully connected")
        except:
            print("Couldn't connect")
        return client

    def insert(self, attr):
        client = self.establishConnection()
        db = client[self.__class__.dbname]
        coll = db[self.get_collection()]
        try:
            coll.insert(attr)
            print "insertion succesful"
        except Exception as e:
            print e

    def loginQuery(self, empid):
        client = self.establishConnection()
        db = client[self.__class__.dbname]
        # collection_name =
        collection = db[self.get_collection()]
        result = collection.find({"empid": empid}, {"PassHash": 1})
        return result

    def query(self, queryString, Projection=None):
        client = self.establishConnection()
        db = client[self.__class__.dbname]
        coll = db[self.get_collection()]
        result = coll.find(queryString, Projection)
        return result
    #
    # def getKey(self, user):
    #     querystring = {"empid": user}
    #     projection = {"key": 1}
    #     return self.query(querystring, projection)
