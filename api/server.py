from encodings import utf_8
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from json import dumps
from scrapingPanelinha import *

app = Flask(__name__)

@app.route('/search')
def do_search():
    palavra = request.args.get('receita')
    olar = getSearchResult(palavra)
    return olar

@app.route('/recipe')
def open_recipe():
    slug = request.args.get('receita')
    olar = getRecipe(slug)
    return olar



if __name__ == '__main__':
    app.run()