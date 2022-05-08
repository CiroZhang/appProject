from System.Websites import Websites


item = ""
web = Websites()
web.remove_keyword()

web.add_skinnytaste(item)
web.add_food52(item)
web.add_allrecipes(item)

web.sort_counts(True)  # sort data from largest to smallest

web.setUp_graph(40)  # limits how much result is shown

web.print_pie_chart()
print(web.graph)
# print(web.dumped)  # shows unused data


# data.write()
# data.close()
