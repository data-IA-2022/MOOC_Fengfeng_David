from colorama import Fore, Back, Style
def message_count(obj):
    '''
    This function must return the number of message
    Parameters: 
        Objet json
    Return:
        Number of message
    '''
    cumul = 1
    depth = obj['depth'] if 'depth' in obj else -1
    print(f"{'  ' * (depth+1)}id: {Fore.RED}{obj['id']}{Style.RESET_ALL}, depth: {depth}, count: {obj['comments_count'] if 'comments_count' in obj else '-'}")
    for msg in obj['children']:
        cumul += message_count(msg)
    print(f"id: {obj['id']} : {cumul} messages")
    return cumul

def factorielle(n):
    if n == 1: return 1
    else:
        resultat = n * factorielle(n-1)
        return resultat
    