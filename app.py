

from flask import Flask, jsonify, request, render_template, redirect
import json, utils, yaml
from sqlalchemy import create_engine
from pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from utils import get_config


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
    id = StringField('id', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])

@app.route("/", methods=['POST', 'PUT', 'GET'])
def index():
    #return redirect("/mongo/52ef5cb2d75e29d72b00098e")
    return render_template('index.html')

@app.route('graph', methods=['POST', 'PUT', 'GET'])
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print('validate_on_submit !', form)
        return redirect('/mongo/xxx')
    return render_template('submit.html', form=form)

@app.route("/mongo", methods=['GET', 'POST'])
def demo_mongo():
    print(f"demo_mongo, args={request.form}")
    filter={
        '_id': request.form.get('id'),
    }
    project={
        'annotated_content_info': 0
    }

    result = client['DEMO']['forum'].find_one(
        filter=filter,
        projection=project
    )
    #print(f"result={result}")

    return render_template('demo1.html', result=result), 202


if __name__ == "__main__":
    app.run(debug=True, port=4000, host='0.0.0.0')