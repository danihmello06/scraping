import urllib.request
import requests
from bs4 import BeautifulSoup

class SearchResult:
    def __init__(self, slug, imageUrl, title):
        self.slug = slug
        self.imageUrl = imageUrl
        self.title = title

class Recipe:
    def __init__(self, title, imageUrl, slug, author, serves, prepareTime, steps):
        self.title = title
        self.imageUrl = imageUrl
        self.slug = slug
        self.author = author
        self.serves = serves
        self.prepareTime = prepareTime
        self.steps = steps

class Steps:
    def __init__(self, title, ingredients, preparation):
        self.title = title
        self.ingredients = ingredients
        self.preparation = preparation

def getSearchResult(word):
    
    searchUrl = "https://panelinha-api-server-prod.herokuapp.com/v1/search?pageSize=1000&title="+word
    searchRequest = requests.get(searchUrl).json()

    searchList = []
    results = searchRequest['data']['results']
    for i in range(len(results)):
        slug = results[i]['slug']
        imageUrl = results[i]['imageUrl']
        title = results[i]['title']
        recipeFound = SearchResult(slug, imageUrl, title)
        
        if results[i]['imageFolder'] == 'receita':
            searchList.append(recipeFound.__dict__)

    return searchList

def getRecipe(slug):
    
    urlBS = "https://www.panelinha.com.br/receita/"+slug
    page = urllib.request.urlopen(urlBS)
    pageBS = BeautifulSoup(page, 'html.parser')
    
    base = pageBS.find_all('div', attrs={'class': 'col-xs-12 col-sm-6 col-md-7'})
    ingredientsAndInstructions = base[1].findAll('div', class_='editor ng-star-inserted')
    ingredientsList = []

    for i in range(0, len(ingredientsAndInstructions), 3):
        ingredientsOnly = ingredientsAndInstructions[i].findAll('li', class_='ng-star-inserted')
        ingredientsInIntruction = []
        for ing in ingredientsOnly:
            ingredientsInIntruction.append(ing.text)
        ingredientsList.append(ingredientsInIntruction)
    
    recipeUrl = "https://panelinha-api-server-prod.herokuapp.com/v1/receita/"+slug
    recipeRequest = requests.get(recipeUrl).json()
    result = recipeRequest['data']
    content = result['content']
    recipeSteps = content['recipeSteps']
    stepsUpdated = []
    for i in range(len(recipeSteps)):
        if 'ingredients' in recipeSteps[i]:
            stepsUpdated.append(recipeSteps[i])
    
    stepsList = []
    for i in range(len(stepsUpdated)):
        stepPreparation = stepsUpdated[i]['body']
        formattedStepPreparation = BeautifulSoup(stepPreparation, 'html.parser').getText()
        steps = Steps(
            stepsUpdated[i]['title'],
            ingredientsList[i],
            formattedStepPreparation
        )
        stepsList.append(steps.__dict__)
    
    recipe = Recipe(
        result['title'], 
        result['imageUrl'], 
        result['slug'], 
        content['author'], 
        content['serves'], 
        content['prepareTime'],
        stepsList
    )
    
    return recipe.__dict__
