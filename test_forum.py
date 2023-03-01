import json, colorama
from utils import factorielle, message_count
from pymongo import MongoClient
def test_forum():
    with open('datasets/sample.json') as f:
        for line in f:
            x = json.loads(line)
            assert x != None
            print('----------------------------------------------------')
            n = message_count(x['content'])
            assert n == x['content']['comments_count']+1

def test_fact():
    n = factorielle(1)
    assert n == 1
    n = factorielle(2)
    assert n == 2
    n = factorielle(3)
    assert n == 6
    n = factorielle(4)
    assert n == 24
    
def test_mongo():
    url = 'mongodb://localhost:27017'
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    