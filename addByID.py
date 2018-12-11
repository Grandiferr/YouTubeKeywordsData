from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['KC']
ytChannelCollection = db["ytChannelCollection"]
def addByID(ID):
    
