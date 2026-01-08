from pymongo import AsyncMongoClient

mongo_client: AsyncMongoClient = AsyncMongoClient(
  "mongodb://admin:admin@mongo:27017/?authSource=admin")