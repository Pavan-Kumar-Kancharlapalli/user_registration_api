

from pymongo import MongoClient
 
mongo_url = "mongodb+srv://username:password@database.g2h69bg.mongodb.net/"
db_name = "userdb"
sampled_data = "users"
tokens= "tokens"
 
client = MongoClient(mongo_url)
database = client[db_name]
user_collection = database[sampled_data]
token_collection = database[tokens]
