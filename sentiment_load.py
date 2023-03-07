import pandas as pd
import numpy as np
from langdetect import detect
from sqlalchemy import create_engine
from utils import get_config
from textblob import TextBlob as tb
from textblob_fr import PatternTagger, PatternAnalyzer
from IPython.display import display

def detect_lang(text):
  try:
    return detect(text)
  except Exception:
    return np.nan

def get_polarity(text):
  lang = detect_lang(text)
  blob = tb(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
  if lang == "en":
    try:
      return tb(text).sentiment.polarity
    except Exception:
      return np.nan
  elif lang == "fr":
    try:
      return blob.sentiment[0]
    except Exception:
      return np.nan
  else:
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
    return np.nan

def main():
    engine = create_engine(get_config('mysql'))
    print(engine)
    df = pd.read_sql("Select username, body, id from Message;", engine)
    for (i, row) in df.iterrows():
      if i>10: quit()
      print(i, row)

if __name__=='__main__':
    main()