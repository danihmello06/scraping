from flask import Flask, request
from scrapingPanelinha import *
from policy import *

app = Flask(__name__)

@app.route('/search')
def do_search():
    searched_word = request.args.get('word')
    return get_search_result(searched_word)

@app.route('/recipe')
def open_recipe():
    slug = request.args.get('slug')
    return get_recipe(slug)

@app.route('/policy')
def open_policy():
    return get_policy()

if __name__ == '__main__':
    app.run()