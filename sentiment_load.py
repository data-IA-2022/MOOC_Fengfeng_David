import pandas as pd
import numpy as np
from polyglot.detect import Detector
from polyglot.text import Text
from textblob import TextBlob as tb
from textblob_fr import PatternTagger, PatternAnalyzer
from IPython.display import display
from utils import relative_path, connect_ssh_tunnel, connect_to_db

def detect_lang(text):
  try:
    detect = Detector(text)
    return detect.language.code
  except Exception:
    return None

def get_polarity(text):
  lang = detect_lang(text)
  text_analysed = Text(text, hint_language_code=lang)
  try:
    return text_analysed.polarity
  except Exception:
    return None

def get_subjectivity(text):
  lang = detect_lang(text)
  blob = tb(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
  if lang == "en":
    try:
      return tb(text).sentiment.subjectivity
    except Exception:
      return None
  elif lang == "fr":
    try:
      return blob.sentiment[1]
    except Exception:
      return None
  else:
    return None
      
      
def get_analysis(score):
  if score < 0:
    return "Negatif"
  elif score == 0:
    return "Neutre"
  else:
    return "Positif"
  
def get_analysis2(score):
  if score <= 0.5:
    return "Objectif"
  elif score > 0.5:
    return "Subjectif"
  else:
    return None

def main():
    config_file = relative_path("config.yml")
    sshtunnel_mysql = connect_ssh_tunnel(config_file, "ssh_mysql")
    engine = connect_to_db(config_file, "database_mysql")
    print(engine)
    df = pd.read_sql("Select body, id from Message;", engine)
    for (i, row) in df.iterrows():
      print(i)
      polarity = get_polarity(row['body'])
      subjectivity = get_subjectivity(row['body'])
      engine.execute("UPDATE Message SET polarity=%s, subjectivity=%s WHERE id=%s ;", [polarity, subjectivity, row['id']])

if __name__=='__main__':
    main()