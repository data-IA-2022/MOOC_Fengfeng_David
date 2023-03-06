from pymongo import MongoClient
from sqlalchemy import create_engine
from utils import get_config, recur_message
from pprint import pprint
import re

# But remplir la table Result de la base de données
# work in progress

def main():
    client = MongoClient(get_config("mongo"))
    engine = create_engine(get_config("mysql"))
    db = client['g3-MOOC']
    user = db['user']
    
    doc = user.find({}).limit(50)
    for dic in doc:
        for key, value in dic.items():
            if value!={} and value!=None:
                if type(value) is str:
                    print(value)
                elif type(value) is dict:
                    for key2, value2 in value.items():
                        print(f"key : {key2}, value : {value2}")
    
if __name__=='__main__':
    main()
