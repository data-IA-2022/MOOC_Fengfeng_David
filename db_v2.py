import time
from unidecode import unidecode
from pymongo import MongoClient
from sqlalchemy import MetaData, create_engine
from sqlalchemy.dialects.mysql import insert
from utils import calc_time, get_config

# Ne fonctionne pas
def recur_message(msg, f, thread_id, parent_id = None, course_id=None):
    '''
    Cette fonction fait un traitement messages de l'objet JSON passé
    :param obj: objet JSON contiens un MESSAGE
    :param f: fonctions à appeler
    :return:
    '''
    #print("Recurse ", obj['id'], obj['depth'] if 'depth' in obj else '-')

    f(msg, thread_id, parent_id, course_id)

    if 'children' in msg:
        for child in msg['children']:
            recur_message(child, f, thread_id, parent_id = msg['id'], course_id=msg['course_id'])

    if 'non_endorsed_responses' in msg:
        for child in msg['non_endorsed_responses']:
            recur_message(child, f, thread_id, parent_id = msg['id'], course_id=msg['course_id'])

    if 'endorsed_responses' in msg:
        for child in msg['endorsed_responses']:
            recur_message(child, f, thread_id, parent_id = msg['id'], course_id=msg['course_id'])


def traitement(msg, thread_id, parent_id=None, course_id=None):
    '''
    Effectue un traitement sur l'obj passé (Message)
    :param msg: Message
    :return:
    '''

    dt = msg['created_at']
    dt = f"{dt[:10]} {dt[11:19]}"

    data_insert = {
        'id':           msg['id'],
        'type':         msg['type'],
        'created_at':   dt,
        'username':     msg['username'] if 'username' in msg else None,
        'depth':        msg['depth'] if 'depth' in msg else None,
        'body':         msg['body'],
        'course_id':    course_id,
        'parent_id':    parent_id,
        'thread_id':    thread_id,
    }

    if not msg['anonymous'] and not msg['anonymous_to_peers']:
        stmts['User'].append({
            'username':             msg['username'],
            'user_id':              msg['user_id'],
            'country':              None,
            'gender':               None,
            'education_level':      None,
            'city':                 None,
            'year_of_birth':        None,
        })

    stmts['Message'].append(data_insert)

    # mysqlEngine.execute("""INSERT INTO Messages
    #                     (id, type, created_at, user_id, depth, body, parent_id) 
    #                     VALUES (%s,%s,%s,%s,%s,%s,%s)
    #                     ON DUPLICATE KEY UPDATE parent_id=VALUES(parent_id), depth=VALUES(depth);""",
    #                     [msg['id'], msg['type'], dt, user_id, msg['depth'] if 'depth' in msg else None, msg['body'], parent_id])


def traitement_user(doc):

    gender              = None
    year_of_birth       = None
    city                = None
    country             = None
    level_of_education  = None

    na = ('None', 'none', 'N', 'N/A', '', ' ', None)

    for key in doc:
        if key in ('_id', 'id', 'username', 'data'): continue

        stmts['Course'].append({'id': key})

        if 'grade' in doc[key] and 'Certificate Eligible' in doc[key]:
            stmts['Result'].append({'course_id': key, 'username': doc['username'], 'grade': doc[key]['grade'], 'eligibility': doc[key]['Certificate Eligible']})

        if 'gender' in doc[key]:
            gender = unidecode(doc[key]['gender']).lower() if doc[key]['gender'] not in na else gender

        if 'year_of_birth' in doc[key]:
            year_of_birth = doc[key]['year_of_birth'] if doc[key]['year_of_birth'] not in na else year_of_birth

        if 'city' in doc[key]:
            city = unidecode(doc[key]['city']).lower() if doc[key]['city'] not in na else city

        if 'country' in doc[key]:
            country = unidecode(doc[key]['country']).lower() if doc[key]['country'] not in na else country

        if 'level_of_education' in doc[key]:
            level_of_education = unidecode(doc[key]['level_of_education']).lower() if doc[key]['level_of_education'] not in na else level_of_education

    stmts['User'].append({
        'username':             doc['username'],
        'user_id':              doc['_id'],
        'gender':               gender,
        'year_of_birth':        year_of_birth,
        'city':                 city,
        'country':              country,
        'education_level':      level_of_education,
    })


def traitement_forum(doc):

    stmts['Course'].append({'id': doc['content']['course_id']})
    stmts['Thread'].append({'_id': doc['_id'], 'course_id': doc['content']['course_id'], 'title': doc['content']['title'], 'comments_count': doc['content']['comments_count']})

    recur_message(doc['content'], traitement, doc['_id'])


def boucles(cursor, boucle, name_print, len_cursor, print_insert = False):

    print(f"\n ----- {name_print}\n")

    n = 0
    perc = 0
    if print_insert :
        len_stmt = sum([len(stmts[key]) for key in stmts])
    total_time = time.time()
    t = time.time()

    for doc in cursor:

        boucle(doc)

        n += 1
        n_perc = int(n / len_cursor * 100)

        if perc // 10 != n_perc // 10:

            perc = n_perc

            str_insert = f"({sum([len(stmts[key]) for key in stmts]) - len_stmt:7} inserts) " if print_insert else ""
            print(f" - {perc:3} %   {name_print:10} {str_insert}  {calc_time(t)}")

            t = time.time()

            if print_insert:
                len_stmt = sum([len(stmts[key]) for key in stmts])

    print(f"--- {name_print} TIME : {calc_time(total_time)}")

#config_file = relative_path("config_direct.yml")

#sshtunnel_mongodb = connect_ssh_tunnel(config_file, "ssh_mongodb")
#sshtunnel_mysql = connect_ssh_tunnel(config_file, "ssh_mysql")

mongoClient = MongoClient(get_config('mongo'))
mysqlEngine = create_engine(get_config('mysql'))
mysqlConn = mysqlEngine.connect().execution_options(isolation_level="AUTOCOMMIT")
mysqlConn.begin()

print(mongoClient)
print(mysqlEngine)

META = MetaData()
META.reflect(bind=mysqlEngine)

stmts = {
    'Course': [],
    'Message': [],
    'Result': [],
    'Thread': [],
    'User': [],
}

db = mongoClient['g3-MOOC']
global_time = time.time()

print(f"\n ----- DOWNLOAD DATA FROM MONGO", end='')

t = time.time()

cursor_user = db['user'].find()
cursor_forum = db['forum'].find()

print(f" / TIME : {calc_time(t)}")

boucles(cursor_user, traitement_user, "user", len(list(cursor_user.clone())), True)
boucles(cursor_forum, traitement_forum, "forum", len(list(cursor_forum.clone())), True)

tables_in_order = ['Course', 'Message', 'Result', 'Thread', 'User']

for key in tables_in_order:

    total_time = time.time()
    print(f"\n ----- EXECUTE {key.upper():10}", end='')
    #mysqlConn.execute(insert(META.tables[key.strip('_2')]).prefix_with("IGNORE"), stmts[key])
    mysqlConn.execute(insert(META.tables[key.strip('_2')]).prefix_with("IGNORE"), stmts[key])
    print(f" / TIME : {calc_time(total_time)}")

print('\n-------- COMMIT')
mysqlConn.commit()
#conn.commit()
print('\n-------- END')

print(f"\nTOTAL INSERT COUNT : {sum([len(stmts[key]) for key in stmts])}\n")

print(f"\nGLOBAL TIME : {calc_time(global_time)}")