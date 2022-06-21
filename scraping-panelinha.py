import urllib.request
import requests
from bs4 import BeautifulSoup
import json

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


finalUrl = "https://www.panelinha.com.br/receita/Torta-integral-de-frango-com-espinafre"
page = urllib.request.urlopen(finalUrl)
receita = BeautifulSoup(page, 'html.parser')
   
base = receita.find_all('div', attrs={'class':'col-xs-12 col-sm-6 col-md-7'})

titulos = base[1].findAll('h4', class_='green h__header')
ingredEPreparo = base[1].findAll('div', class_='editor ng-star-inserted')

ingredients = []

for i in range(0, len(ingredEPreparo), 3):
    ing = ingredEPreparo[i].findAll('li', class_='ng-star-inserted')
    listaIngredientes1 = []
    for ing in ing:
        listaIngredientes1.append(ing.text)
    ingredients.append(listaIngredientes1)

searchRequest = requests.get("https://panelinha-api-server-prod.herokuapp.com/v1/search?pageSize=1000&title=bolo").json()

searchList = []
results = searchRequest['data']['results']
for i in range(len(results)):
    slug = results[i]['slug']
    imageUrl = results[i]['imageUrl']
    title = results[i]['title']
    single = SearchResult(slug, imageUrl, title)
    searchList.append(single.__dict__)

jsonstr1 = json.dumps(searchList, ensure_ascii=False)
jsonFile = open("SearchResultData.json", "w", encoding="utf-8")
jsonFile.write(jsonstr1)
jsonFile.close()

########### RECIPE DATA
recipeRequest = requests.get("https://panelinha-api-server-prod.herokuapp.com/v1/receita/Torta-integral-de-frango-com-espinafre/null").json()
result = recipeRequest['data']
content = result['content']
recipeSteps = content['recipeSteps']

for i in range(len(recipeSteps)):
    if 'ingredients' not in recipeSteps[i]:
        recipeSteps.remove(recipeSteps[i])

stepsList = []
for i in range(len(recipeSteps)):
    steps = Steps(
        recipeSteps[i]['title'],
        ingredients[i],
        recipeSteps[i]['body']
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

jsonstr2 = json.dumps(recipe.__dict__, ensure_ascii=False)
jsonFile2 = open("RecipeData.json", "w", encoding="utf-8")
jsonFile2.write(jsonstr2)
jsonFile2.close()