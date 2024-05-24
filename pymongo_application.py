import pymongo
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# Conectando ao MongoDB

client = pymongo.MongoClient(os.environ.get('MONGO_CONNECTION_STRING'))

db = client.bank

clients = db.clients

user1 = {
    "name": "João",
    "cpf": "123.456.789-00",
    "address": "Street A, 123",
    "account": [
        {
            "type": "current",
            "agency": "0001",
            "num": "123456-7",
            "balance": 1000.00
        }
    ]
}

user2 = {
    "name": "Maria",
    "cpf": "987.654.321-00",
    "address": "Street B, 456",
    "account": [
        {
            "type": "current",
            "agency": "0001",
            "num": "123457-7",
            "balance": 2000.00
        }
    ]
}


joao = clients.insert_one(user1)
maria = clients.insert_one(user2)

all_clients = clients.find()
for client in all_clients:
    pprint(client)


clients.update_one({"_id": joao.inserted_id}, {
                   "$set": {"name": "João da Silva"}})

print(clients.find_one({"_id": joao.inserted_id}))
