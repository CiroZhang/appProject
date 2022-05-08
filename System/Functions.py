import json
import requests
from bs4 import BeautifulSoup


def setUpIngredientListJson():
    file = open("Data/ingredient_list.json", "w")
    data = {}
    response = requests.get("https://world.openfoodfacts.org/entry-date/2016-08/ingredients")
    soup = BeautifulSoup(response.content, 'html.parser')
    lists = soup.findAll('a', attrs={'class': 'tag known'})

    for item in lists:
        item = item.text.lower()
        if item.find(":") > 0:
            item = item[item.find(":") + 1:]
        data[item] = 0
    file.write(json.dumps(data.item_counts, indent=4, sort_keys=True))

    setUpIngredientListJson()
