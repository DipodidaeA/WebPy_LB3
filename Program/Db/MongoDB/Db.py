from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

dbmo = client["wether_app_mo"]