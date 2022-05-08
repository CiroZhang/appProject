from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.lang import builder, Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from System.Websites import Websites

item_list = []
web = Websites()
web.remove_keyword()


class SearchWindow(Screen):
    item = ObjectProperty(None)

    def addItem(self):
        item_list.append(self.item.text)
        self.item.text = ""
        print(item_list)

    def submit(self):
        for i in item_list:
            web.add_skinnytaste(i)
            web.add_food52(i)
            web.add_allrecipes(i)
        web.sort_counts(True)  # sort data from largest to smallest

        web.setUp_graph(30)  # limits how much result is shown

        web.print_pie_chart()
        print(web.graph)


class SecondWindow(Screen):
    results = ObjectProperty(None)

    def update(self):
        self.results.text = str(web.graph)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('design.kv')


class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()
