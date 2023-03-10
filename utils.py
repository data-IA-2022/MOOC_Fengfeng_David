import time
import numpy as np
from os.path import dirname, join
from textblob import TextBlob as tb
from textblob_fr import PatternTagger, PatternAnalyzer
import yaml
from sshtunnel import SSHTunnelForwarder
from polyglot.detect import Detector
from polyglot.downloader import downloader
from polyglot.text import Text

def relative_path(*path):

    return join(dirname(__file__), *path)


def calc_time(start_time):

    d = time.time() - start_time
    h = int(d / 3600)
    h = f"{h} h " if d > 3600 else ''
    m = int(d % 3600 / 60)
    m = f"{m:02} m " if d >= 3600 else f"{m} m " if d > 60 else ''
    s = int(d % 3600 % 60)
    s = f"{s:02} s" if d >= 60 else f"{s} s"
    return h + m + s


def connect_ssh_tunnel(config_file, section):

    # Read configuration information from file
    config = yaml.safe_load(open(config_file, 'r'))

    ssh_config = config[section]

    server = SSHTunnelForwarder(
        ssh_config['host'],
        ssh_username = ssh_config['user'],
        ssh_password = ssh_config['password'],
        remote_bind_address = (ssh_config['remote_adr'], ssh_config['remote_port']),
        local_bind_address = (ssh_config['local_adr'], ssh_config['local_port'])
    )

    server.start()

    return server


def connect_to_db(config_file, section):

    # Read configuration information from file
    config = yaml.safe_load(open(config_file, 'r'))

    url_pswd = ":{password}".format(**config[section]) if config[section]["password"] != None else ""
    url_user = "{user}{url_pswd}@".format(**config[section], url_pswd = url_pswd) if config[section]["user"] != None else ""
    url_port = ":{port}".format(**config[section]) if config[section]["type"] != "mongodb" else ""
    url_data = "/{db_name}".format(**config[section]) if config[section]["db_name"] != None else ""

    url = "{type}://{url_user}{host}{url_port}{url_data}".format(**config[section], url_user=url_user, url_port=url_port, url_data=url_data)

    if config[section]["type"] == "mongodb":

        from pymongo import MongoClient
        from pymongoarrow.monkey import patch_all

        patch_all()

        return MongoClient(url, config[section]["port"])

    else:

        from sqlalchemy import create_engine

        return create_engine(url, future=True)
    
def get_config(cnx):
    config_file = relative_path("config_direct.yml")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    cfg=config[cnx]
    if cnx == 'mysql':
        return "{driver}://{user}:{password}@{host}:{port}/{database}".format(**cfg)
    elif cnx == 'mongo':
        return "{driver}://{host}:{port}".format(**cfg)
    
def detect_lang(text):
  try:
    detect = Detector(text)
    return detect.language.code
  except Exception:
    return np.nan

def get_polarity(text):
  lang = detect_lang(text)
  text_analysed = Text(text, hint_language_code=lang)
  try:
    return text_analysed.polarity
  except Exception:
    return np.nan
      
def get_subjectivity(text):
  lang = detect_lang(text)
  blob = tb(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
  if lang == "en":
    try:
      return tb(text).sentiment.subjectivity
    except Exception:
      return np.nan
  elif lang == "fr":
    try:
      return blob.sentiment[1]
    except Exception:
      return np.nan
  else:
    return np.nan