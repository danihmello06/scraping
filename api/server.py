from flask import Flask, request
from scrapingPanelinha import *

app = Flask(__name__)

@app.route('/search')
def do_search():
    searchedWord = request.args.get('word')
    return getSearchResult(searchedWord)

@app.route('/recipe')
def open_recipe():
    slug = request.args.get('slug')
    return getRecipe(slug)

if __name__ == '__main__':
    app.run()
    
    #app.run(host="0.0.0.0")