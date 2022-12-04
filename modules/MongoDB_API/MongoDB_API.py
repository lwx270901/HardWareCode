import os
import pprint
from pymongo import MongoClient

class mongo_dbs:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.test_db = self.client[db_name]

    def insert_test_doc(self, collection_name, document):
        collection = self.test_db[collection_name]
        inserted_id = collection.insert_one(document).inserted_id
        return inserted_id

    def update_test_doc(self, collection_name, document):
        pass

    def read_test_doc(self, id):
        pass

    def get_QR_code(self, collection_name, id):
        from bson.objectid import ObjectId
        collection = self.test_db[collection_name]

        _id = ObjectId(id)
        obj = collection.find_one({"_id": _id})
        return obj


    def delete_test_doc(self, id):
        pass
    

# client = MongoClient("mongodb+srv://shineinouzen:viper270901@dacn.ncyeov0.mongodb.net/?retryWrites=true&w=majority")
# db = client["Server"]
# collection = db["event"]
# PkI6a3nf5faU9Hil
# document = {
#     "time":"Adfaf",
#     "image":"afeawf"
# }
# # collection.insert_one(document)

# mg = mongo_dbs("mongodb+srv://minh:minh@server.tdyzh9j.mongodb.net/?retryWrites=true&w=majority", "DB")
# ex = mg.get_QR_code("users", "638b7d621f8781fa9278893e")

# print(ex)