from colorama import Fore, Back, Style
from yaml import safe_load

def message_count(obj):
    '''
    This function must return the number of message
    Parameters: 
        Objet json
    Return:
        Number of message
    '''
    cumul = 1
    depth = obj['depth'] if 'depth' in obj else "-"
    print(f"{'  ' * (depth+1)}id: {Fore.RED}{obj['id']}{Style.RESET_ALL}, depth: {depth}, count: {obj['comments_count'] if 'comments_count' in obj else '-'}")
    if 'children' in obj:
        for msg in obj['children']:
            cumul += message_count(msg)
    if 'non_endorsed_responses' in obj:
        for msg in obj['non_endorsed_responses']:
            cumul += message_count(msg)
    if 'endorsed_responses' in obj:
        for msg in obj['endorsed_responses']:
            cumul += message_count(msg)
    print(f"id: {obj['id']} : {cumul} messages")
    return cumul

def factorielle(n):
    if n == 1: return 1
    else:
        resultat = n * factorielle(n-1)
        return resultat
    
def recur_message(obj, f, parent_id=None):
    '''
    This function must return the number of message
    Parameters: 
        Objet json
    Return:
        Number of message
    '''
    f(obj, parent_id)
    if 'children' in obj:
        for msg in obj['children']:
            recur_message(msg, f, parent_id=obj['id'])
    if 'non_endorsed_responses' in obj:
        for msg in obj['non_endorsed_responses']:
            recur_message(msg, f, parent_id=obj['id'])
    if 'endorsed_responses' in obj:
        for msg in obj['endorsed_responses']:
            recur_message(msg, f, parent_id=obj['id'])
            
def get_config(cnx):
    with open('config.yml', 'r') as f:
        config = safe_load(f)
    cfg=config[cnx]
    if cnx == 'mysql':
        return "{driver}://{user}:{password}@{host}:{port}/{database}".format(**cfg)
    elif cnx == 'mongo':
        return "{driver}://{host}:{port}".format(**cfg)