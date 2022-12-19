import requests
from bs4 import BeautifulSoup
from operator import itemgetter

class SearchResult:
    def __init__(self, author, image_url, index, slug, title):
        self.author = author
        self.image_url = image_url
        self.index = index
        self.slug = slug
        self.title = title

class Recipe:
    def __init__(self, title, image_url, slug, author, serves, prepare_time, steps):
        self.title = title
        self.image_url = image_url
        self.slug = slug
        self.author = author
        self.serves = serves
        self.prepare_time = prepare_time
        self.steps = steps

class Steps:
    def __init__(self, title, ingredients, preparation):
        self.title = title
        self.ingredients = ingredients
        self.preparation = preparation

def get_search_result(word):
    
    result_from_panelinha = get_search_from_panelinha(word)
    all_lists_combined = order_results_equally(result_from_panelinha)

    return all_lists_combined

def get_search_from_panelinha(word):

    search_url = "https://panelinha-api-server-prod.herokuapp.com/v1/search?pageSize=1000&title="+word
    search_request = requests.get(search_url).json()

    search_list = []
    results = search_request['data']['results']
    for i in range(len(results)):
        author = "panelinha"
        image_url = results[i]['imageUrl']
        index = i
        slug = results[i]['slug']
        title = results[i]['title']
        recipe_found = [author, image_url, index, slug, title]
        
        if results[i]['imageFolder'] == 'receita':
            search_list.append(recipe_found)

    return search_list

def order_results_equally(all_lists_combined):
    sorted_list = sorted(all_lists_combined, key = itemgetter(2))
    list_of_search_result = []
    for i in range(len(sorted_list)):
        search_item = SearchResult(
            author = sorted_list[i][0],
            image_url = sorted_list[i][1],
            index = sorted_list[i][2],
            slug = sorted_list[i][3],
            title = sorted_list[i][4]
        )
        list_of_search_result.append(search_item.__dict__)        
    return list_of_search_result

def get_recipe_from_panelinha(slug):
    url_bs = "https://www.panelinha.com.br/receita/"+slug
    data = requests.get(url_bs)
    page_bs = BeautifulSoup(data.content, 'html.parser')
    
    base = page_bs.find_all('div', attrs={'class': 'col-xs-12 col-sm-6 col-md-7'})
    ingredients_and_instructions = base[1].findAll('div', class_='editor ng-star-inserted')
    ingredients_list = []

    for i in range(0, len(ingredients_and_instructions), 3):
        ingredients_only = ingredients_and_instructions[i].findAll('li', class_='ng-star-inserted')
        ingredients_in_intruction = []
        for ing in ingredients_only:
            ingredients_in_intruction.append(ing.text)
        ingredients_list.append(ingredients_in_intruction)
    
    recipe_url = "https://panelinha-api-server-prod.herokuapp.com/v1/receita/"+slug
    recipe_request = requests.get(recipe_url).json()
    result = recipe_request['data']
    content = result['content']
    recipe_steps = content['recipeSteps']
    steps_updated = []
    for i in range(len(recipe_steps)):
        if 'ingredients' in recipe_steps[i]:
            steps_updated.append(recipe_steps[i])
    
    steps_list = []
    for i in range(len(steps_updated)):
        step_preparation = steps_updated[i]['body']
        formatted_step_preparation = BeautifulSoup(step_preparation, 'html.parser').getText()
        steps = Steps(
            steps_updated[i]['title'],
            ingredients_list[i],
            formatted_step_preparation
        )
        steps_list.append(steps.__dict__)
    
    recipe = Recipe(
        result['title'], 
        result['imageUrl'], 
        result['slug'], 
        content['author'], 
        content['serves'], 
        content['prepareTime'],
        steps_list
    )

    return recipe

def get_recipe(slug, author):

    recipe = Recipe("","","","","","","")
    if author == "panelinha":
        recipe = get_recipe_from_panelinha(slug)

    return recipe.__dict__
    