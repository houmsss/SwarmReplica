import mongo
from datetime import datetime

from flask import Flask

connection = mongo.connect('university-mongo-swarm', 27017, 'mongodbuser', 'your_mongodb_root_password')
database = mongo.use(connection, '1')
collection = mongo.pick_collection(database, '1')
  
app = Flask(__name__)

def get_hit_count():
  doc = mongo.find_document(collection, {})
  if (doc and 'count' in doc):
    mongo.update_document(collection, { '_id': doc['_id'] }, { 'count': int(doc['count']) + 1 , 'time': datetime.now() })
    return doc['count'] + 1
  else:
    mongo.insert_document(collection, { 'count': 1 , 'time': datetime.now() })
    return 1

@app.route('/')
def hello():
  count = get_hit_count()
  return 'Hello World! I have been seen {} times.\n'.format(count)
