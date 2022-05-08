import json

import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

file = open("ingredient_list.json", "r")
item_list = []


class Data:
    def __init__(self):
        self.adjusted = True
        self.item_counts = json.load(file)
        self.graph = "not set"
        self.dumped = []

    def remove_keyword(self):
        pass

    def add_count(self, item):
        items = item.split("and") if item.find("and") > 0 else [item]
        for item in items:
            if item in self.item_counts:
                self.item_counts[item] += 1
            else:
                self.dumped.append(item)

    def sort_counts(self, reverse=False):
        self.item_counts = dict(sorted(self.item_counts.items(), key=lambda x: x[1], reverse=reverse))

    def setUp_graph(self, threshold):
        values = []
        names = []
        threshold -= 1
        other_count = 0
        x = 0
        for i in self.item_counts:
            if x < threshold:
                names.append(i)
                values.append(self.item_counts[i])
            else:
                other_count += self.item_counts[i]
            x = x + 1
        values.append(other_count)
        names.append("other")
        self.graph = pd.DataFrame({'count': values}, index=names)

    def print_pie_chart(self):
        self.graph.plot.pie(y='count', figsize=(50, 50), fontsize=30)
        plt.show()
        plt.close()
