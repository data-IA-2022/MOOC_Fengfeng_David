import pymongo
from utils import message_count
import json

def main():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['MOOC']
    forum = db['forum']
    user = db['user']

    print(f"count : {forum.count_documents({})} conversations")
    print(f"count : {user.count_documents({})} users") 

    for doc in forum.find():
        print('----------------------------------------')
        try:
            message_count(doc['content'])
        except Exception as e:
            print(json.dumps(doc, indent=4))
if __name__=='__main__':
    main()