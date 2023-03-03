from pymongo import MongoClient
from utils import message_count
import json
from sqlalchemy import create_engine
from utils import get_config, recur_message
from pprint import pprint

def process(obj, parent_id=None):
    config_mysql = get_config('mysql')
    url_mysql = "{driver}://{user}:{password}@{host}:{port}/{database}".format(**config_mysql)
    engine = create_engine(url_mysql)
    username = obj['username'] if 'username' in obj else None
    depth = obj['depth'] if 'depth' in obj else None
    date = obj['created_at']
    date = date[:10] + ' ' + date[11:19]
    if not obj['anonymous']:
        query_user = "INSERT IGNORE INTO User (username, user_id) VALUES (%s,%s)"
        query_message = """INSERT INTO Message 
                        (id, type, created_at,parent_id, username, body, depth) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY 
                        UPDATE parent_id=VALUES(parent_id), depth=VALUES(depth);"""
        engine.execute(query_user, [obj['username'], obj['user_id']])
        engine.execute(query_message, [obj['id'],obj['type'],date,parent_id,username,obj['body'],depth])
        
        
    
def main():
    client = MongoClient(get_config("mongo"))
    engine = create_engine(get_config("mysql"))
    db = client['g3-MOOC']
    forum = db['forum']
    user = db['user']
    

    # print(f"count : {forum.count_documents({})} conversations")
    # print(f"count : {user.count_documents({})} users") 

    # recherche des fils de discussion our le champ 'childre' existe
    # c = 0
    # docs = forum.find({"content.children": {"$exists": False}}, projection={"annotated_content_info": 0})
    # for doc in docs:
    #     pprint(doc['_id'])
    #     c += 1
    # print(f"count :  {c}")
    
    # insert in thread
    
    cursor = forum.find(filter= None, projection={"annotated_content_info": 0}).batch_size(10)
    for doc in cursor:
        print(doc['_id'], doc['content']['course_id'])
        course_id = doc['content']['course_id']
        thread_id = doc['_id']
        query_course = "INSERT IGNORE INTO Course (course_id) VALUES (%s);"
        query_thread = "INSERT IGNORE INTO Thread (_id,course_id) VALUES (%s,%s);"
        engine.execute(query_course, [course_id])
        engine.execute(query_thread, [thread_id, course_id])
        recur_message(doc['content'], process)
        print("--------------------------------------------")
        

    # recherche content.username
    # for doc in forum.find({"content.username": "ambruleaux"}, projection={"_id": 1, 'content': 1}):
    #     print(doc['_id'])
    #     for value in doc['content']:
    #         print(value)
            
    # for doc in forum.find():
    #     print('----------------------------------------')
    #     try:
    #         message_count(doc['content'])
    #     except Exception as e:
    #         print(json.dumps(doc, indent=4))
if __name__=='__main__':
    main()