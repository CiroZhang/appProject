import requests
from bs4 import BeautifulSoup
import tqdm

from System.system import Data


class Websites(Data):
    def __init__(self):
        super().__init__()
        self.data = None

    def add_allrecipes(self, item):
        print("starting add_allrecipes")

        main_link = 'https://www.allrecipes.com'
        search_link = '/search/results/?search='

        response = requests.get(main_link + search_link + item)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.findAll('a', attrs={'class': 'card__titleLink manual-link-behavior'})
        for i in tqdm.trange(len(links)):
            response = requests.get(links[i]['href'])
            soup = BeautifulSoup(response.content, 'html.parser')
            ingredients = soup.findAll('span', attrs={'class': 'ingredients-item-name'})
            for ingredient in ingredients:
                self.add_count(ingredient.text)
        print("Finished add_allrecipes\n" + "-" * 20)

    def add_food52(self, item):
        print("starting add_food52")

        main_link = 'https://food52.com'
        setup_link = '/recipes/search?'
        search_link = 'q='
        page_link = "page="

        response = requests.get(main_link + setup_link + search_link + item)
        soup = BeautifulSoup(response.content, 'html.parser')
        pages = soup.find('span', attrs={'class': 'search-header__count search-header__count--full-text'}).text
        count = int(pages.replace(",", "")[:pages.find(" ")])
        pages = count / 24
        if int(pages) < pages:
            pages += 1

        for page in range(1, int(pages) + 1):

            if page > 1:
                response = requests.get(main_link + setup_link + page_link + str(page) + "&" + search_link + item)
                soup = BeautifulSoup(response.content, 'html.parser')

            links = soup.findAll('h3', attrs={'class': 'collectable__name'})
            for i in tqdm.trange(len(links)):
                response = requests.get(main_link + links[i].find('a')['href'])
                soup = BeautifulSoup(response.content, 'html.parser')
                recipes = soup.find('div', attrs={'class': 'recipe__list recipe__list--ingredients'}).findAll('li')
                for recipe in recipes:
                    data1 = recipe.text.replace("\n\n", "!").replace("\n", "").split("!")

                    if len(data1) > 1:
                        if data1[1]:
                            if data1[1][0].isalpha():
                                x = data1[1].replace('(', ',').find(',')
                                if x < 0:

                                    self.add_count(data1[1])
                                else:

                                    self.add_count(data1[1][:x])

            print(str(page) + " out of " + str(int(pages)) + " pages completed")
        print("done add_food52\n" + "-" * 20)

    def add_skinnytaste(self, item):
        print("starting add_skinnytaste")

        main_link = 'https://www.skinnytaste.com'
        search_link = '/?s='
        page_link = "/page/"

        response = requests.get(main_link + search_link + item)
        soup = BeautifulSoup(response.content, 'html.parser')
        pages = soup.findAll('a', attrs={'class': 'page-numbers'})
        if pages:
            pages = pages[-2].text
        for page in range(1, int(pages) + 1):
            if page > 1:
                response = requests.get(main_link + page_link + str(page) + search_link + item)
                soup = BeautifulSoup(response.content, 'html.parser')

            links = soup.findAll('article', attrs={'class': 'post teaser-post odd'}) + soup.findAll('article', attrs={
                'class': 'post teaser-post even'})
            for i in tqdm.trange(len(links)):
                response = requests.get(links[i].find('a')['href'])
                soup = BeautifulSoup(response.content, 'html.parser')
                recipes = soup.find('ul', attrs={'class': 'wprm-recipe-ingredients'})
                if recipes:
                    recipes = recipes.findAll('li')
                    for recipe in recipes:
                        self.add_count(recipe.text)

            print(str(page) + " out of " + str(int(pages)) + " pages completed")

        print("done add_skinnytaste\n" + "-" * 20)