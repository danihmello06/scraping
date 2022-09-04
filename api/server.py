from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from json import dumps

app = Flask(__name__)

@app.route('/search')
def do_search():
    palavra = request.args.get('receita')
    
    return "hello world"

@app.route('/recipe')
def open_recipe():
    
    return



if __name__ == '__main__':
    app.run()