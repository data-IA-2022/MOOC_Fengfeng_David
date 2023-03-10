
import pickle
from flask import Flask, jsonify, request, render_template, redirect, url_for
import json, utils, yaml
from sqlalchemy import create_engine
from pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from utils import get_config
import pandas as pd
from utils import detect_lang, get_polarity, get_subjectivity
from pycaret.classification import load_model, predict_model

# source venv/bin/activate
# flask --app app run --debug


client = MongoClient(get_config('mongo'))
db = client['g3-forum']
forum = db['forum']
user = db['user']

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class MyForm(FlaskForm):
    message = TextAreaField('msg', validators=[DataRequired()])
    gender = RadioField('gender', validators=[DataRequired()])
    country = SelectField('country', validators=[DataRequired()])
    education = SelectField('education', validators=[DataRequired()])
    submit = SubmitField('submit')

df = pd.read_csv('data.csv').drop('Unnamed: 0', axis=1)

country = [item for item in df['country'].unique()]
LEVEL_EDUCATION=[
("p", "Doctorat"),
("m", "Master ou diplôme professionnel"), 
("b", "Diplôme de premier cycle supérieur"), 
("hs", "Lycéé / enseignement secondaire"), 
("jhs", "Collège / enseignement secondaire inférieur"), 
("none", "Pas de Formation Scolaire"), 
]
COUNTRY=[
    ("MA", "Maroc"),
    ("FR", "France"),
    ("BE", "Belgique"),
    ("CN", "Chine"),
    ('PF', 'Polynésie française'),
    ('RE', 'La Réunion'),
    ('TN', 'Tunisie')
]
@app.route("/", methods=['POST', 'PUT', 'GET'])
def home():
    #return redirect("/mongo/52ef5cb2d75e29d72b00098e")
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if request.method=='POST':
        polarity = get_polarity(request.form['message'])
        subjectivity = get_subjectivity(request.form['message'])
        model = load_model('classification_model')
        data_sub = pd.DataFrame(data=[[
            request.form['gender'],
            ''.join([item[0] for item in LEVEL_EDUCATION if item[1]==request.form['education']]),
            ''.join([item[0] for item in LEVEL_EDUCATION if item[1]==request.form['education']]),
            request.form['message'],
            polarity,
            subjectivity,
        ]], columns=['gender', 'country', 'education_level', 'body', 'polarity', 'subjectivity'])
        prediction = predict_model(model, data=data_sub)
        label = prediction['Label'].values[0]
        score = prediction['Score'].values[0]
        if label==1:
            result = "Eligible"
        elif label==0:
            result = "Non eligible"
        else:
            result = None
        return render_template('submit.html', 
                           countries=[item[1] for item in COUNTRY], 
                           education=[item[1] for item in LEVEL_EDUCATION], 
                           form=form,
                           score=score,
                           result=result)
        
    # show the form, it wasn't submitted
    return render_template('submit.html', 
                           countries=[item[1] for item in COUNTRY], 
                           education=[item[1] for item in LEVEL_EDUCATION], 
                           form=form)


if __name__ == "__main__":
    app.run(debug=True)