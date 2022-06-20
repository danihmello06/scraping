from base64 import encode
from codecs import utf_8_decode, utf_8_encode
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


finalUrl = "https://www.panelinha.com.br/receita/pudim-na-airfryer"
page = urllib.request.urlopen(finalUrl)
receita = BeautifulSoup(page, 'html.parser')
   
base = receita.find_all('div', attrs={'class':'col-xs-12 col-sm-6 col-md-7'})

titulos = base[1].findAll('h4', class_='green h__header')
ingredEPreparo = base[1].findAll('div', class_='editor ng-star-inserted')

#for i in range(len(ingredEPreparo)):
    
ingred1 = ingredEPreparo[0].findAll('li', class_='ng-star-inserted')
listaIngredientes1 = []
for ing in ingred1:
    listaIngredientes1.append(ing.text)
    
ingred2 = ingredEPreparo[3].findAll('li', class_='ng-star-inserted')
listaIngredientes2 = []
for ing in ingred2:
    listaIngredientes2.append(ing.text)
    
ingredients = []
ingredients.append(listaIngredientes1)
ingredients.append(listaIngredientes2)


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
jsonFile = open("testFile.json", "w", encoding="utf-8")
jsonFile.write(jsonstr1)
jsonFile.close()

########### RECIPE DATA
recipeRequest = requests.get("https://panelinha-api-server-prod.herokuapp.com/v1/receita/pudim-na-airfryer/null").json()
result = recipeRequest['data']
content = result['content']
recipeSteps = content['recipeSteps']

stepsList = []
print(len(recipeSteps))
print('------------------')
print(len(ingredients))
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
jsonFile2 = open("testFile2.json", "w", encoding="utf-8")
jsonFile2.write(jsonstr2)
jsonFile2.close()


"""
r1 = Recipe(listaTitulos, ingredients, preparations)


jsonstr1 = json.dumps(r1.__dict__, ensure_ascii=False)
print(jsonstr1)
jsonFile = open("testFile.json", "w", encoding="utf-8")
jsonFile.write(jsonstr1)
jsonFile.close()


preparo1 = ingredEPreparo[2].findAll('li')
listaPreparo1 = []
for prep in preparo1:
    listaPreparo1.append(prep.text)
    
preparo2 = ingredEPreparo[5].findAll('li')
listaPreparo2 = []
for prep in preparo2:
    listaPreparo2.append(prep.text)
    
preparations = []
preparations.append([listaPreparo1, listaPreparo2])

/////////////////////////////////////

baseUrl = 'https://www.panelinha.com.br'
wiki = 'https://www.panelinha.com.br/busca/pudim'
page = urllib.request.urlopen(wiki)
soup = BeautifulSoup(page, 'html.parser')

grupo = soup.find('div', attrs={'class':'row row__grid'})
todosLinks = grupo.find_all('a')

print("---------------------------")
listaFinal = []

for link in todosLinks:
    listaFinal.append(link.get('href'))



"""