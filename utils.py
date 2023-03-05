from yaml import safe_load


def factorielle(n):
    if n == 1: return 1
    else:
        resultat = n * factorielle(n-1)
        return resultat
    
def recur_message(obj, f, parent_id=None, thread_id=None):
    '''
    This function must return the number of message
    Parameters: 
        Objet json
    Return:
        Number of message
    '''
    if not obj['anonymous'] and not obj['anonymous_to_peers']:
        f(obj, parent_id, thread_id)
        if 'children' in obj:
            for msg in obj['children']:
                print(f"+---->{msg['id']}")
                recur_message(msg, f, parent_id=obj['id'],thread_id=thread_id)
        if 'non_endorsed_responses' in obj:
            for msg in obj['non_endorsed_responses']:
                print(f"+---->{msg['id']}")
                recur_message(msg, f, parent_id=obj['id'], thread_id=thread_id)
        if 'endorsed_responses' in obj:
            for msg in obj['endorsed_responses']:
                print(f"+---->{msg['id']}")
                recur_message(msg, f, parent_id=obj['id'], thread_id=thread_id)
            
def get_config(cnx):
    with open('config.yml', 'r') as f:
        config = safe_load(f)
    cfg=config[cnx]
    if cnx == 'mysql':
        return "{driver}://{user}:{password}@{host}:{port}/{database}".format(**cfg)
    elif cnx == 'mongo':
        return "{driver}://{host}:{port}".format(**cfg)