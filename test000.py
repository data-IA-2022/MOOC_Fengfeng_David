import pycaret
import pandas
from pycaret.classification import *


df = pd.read_csv('reussite_classi.csv')
df = df.drop(['Unnamed: 0'], axis=1)
print("df")
# report = setup(data=df, target="eligibility")