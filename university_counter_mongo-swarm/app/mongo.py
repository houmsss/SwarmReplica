import pymongo

def connect (ip, port, username, password):
    return pymongo.MongoClient(ip, port, username=username,
                 password=password)

def use(client, database):
    return client[database]

def pick_collection(db, name):
    return db[name]

def insert_document(collection, data):
    return collection.insert_one(data).inserted_id

def find_document(collection, elements):
    return collection.find_one(elements)

def update_document(collection, query_elements, new_values):
    collection.update_one(query_elements, {'$set': new_values})

def delete_document(collection, query):
    collection.delete_one(query)