import pymongo


mongoclient = pymongo.MongoClient(
    "mongodb://localhost:27017/?directConnection=true")

db = mongoclient['userauth']
userstabel = db['users']


# mydict = {"name": "John", "address": 99}

# x = userstabel.insert_one(mydict)
# print(x.inserted_id)
# print(userstabel.find_one({'_id': x.inserted_id}, ['address']))
