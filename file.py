import json 
from utils import message_count
with open ('datasets/sample.json') as f:
    for line in f:
        x = json.loads(line)
        message_count(x['content'])
        #print(json.dumps(x, indent=4))