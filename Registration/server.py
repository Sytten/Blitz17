import requests
import json
import menu as menu_retriever
from flask import Flask
from flask import request

app = Flask(__name__)


def retrieve_menu(url):
    # url = 'https://raw.githubusercontent.com/pffy/data-mcdonalds-nutritionfacts/master/json/mcd-pretty.json'
    req = requests.get(url)
    menu_raw = req.json()
    menu = dict()

    for item in menu_raw:
        menu[item['ITEM']] = int(item['CAL'])

    return menu


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/receive', methods=["POST"])
def receive():
    json_dict = request.get_json()

    nb_items = int(json_dict['numberOfItems'])
    calories = int(json_dict['calories'])
    menu_url = json_dict['menuUrl']

    with open('data.json') as data_file:
        data = json.load(data_file)

    menu = retrieve_menu(menu_url)
    items = menu_retriever.get_items(menu, nb_items, calories)
    data['answer'] = items

    return json.dumps(data)


if __name__ == '__main__':
    app.run()
