from pymongo import MongoClient
from utils import get_config
from flask import Flask, request, render_template, redirect, jsonify

client = MongoClient(get_config('mongo'))

db = client['g3-MOOC']
forum = db['forum']

print(forum.count_documents({}))

app = Flask(__name__)

@app.route('/', methods=['PUT', 'POST', 'GET'])
def hello():
    return redirect('/demo')


@app.route("/dyn/<id>", methods=['POST', 'PUT', 'GET'])
def dynamic(id):
    print(request.args)
    return f"<p>ID : {id}, x={request.args.get('x')}, y={request.args.get('y')}</p>"

@app.route("/demo", methods=['GET'])
def demo():
    x=123
    return render_template('demo.html', title='mon test', x=x, y='OK !', z=[1,2,3])

@app.route("/json", methods=['POST', 'PUT', 'GET'])
def get_json():
    return jsonify({"x": 100})
    