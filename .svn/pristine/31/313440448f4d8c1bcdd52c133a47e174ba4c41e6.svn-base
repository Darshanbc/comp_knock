import pymongo
import base64
import bson
from bson.binary import Binary 
from urlparse import urlparse
import hashlib

# def establishconnection():
# establish a connection to the database
uri="mongodb://admin:admin@127.0.0.1:27017"
try:
	client = pymongo.MongoClient(uri)
	print("succesfully connected")
except:
	print("Couldn't connect")



# def insert(dbname,attr):
	
db = client["testdb"]
collection = db["users"]
image=(bytes([[1,2],[4,7]]))
attr={}
attr['image']=image
collection.insert(attr)

# result=collection.find({"empid": "e" },{"PassHash":1})
	# try:
# if result:
	# print " present"
# else:
	# print "not present" 
# print dir(result)
# print "result.count() "+str(result.count()) 
# print result.next()["PassHash"]
	# except Exception as e:
	# 	print "empId or password not matched"