import requests
import json
# import jsonify
# from jsonmerge import merge
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/retrieve_menu')
def retrieve_menu():
    url = 'http://xxx.pythonanywhere.com/stripetest'
    data = {'stripeAmount': '199', 'stripeCurrency': 'USD', 'stripeToken': '122', 'stripeDescription': 'Test post'}
    headers = {'Content-Type' : 'application/json'}

    r = requests.post(url, data=json.dumps(data), headers=headers)

    # return json.dumps(r.json(), indent=4)
    return r.text


@app.route('/receive', methods=["POST"])
def receive():
    json_dict = request.get_json()

    nb_items = json_dict['numberOfItems']
    calories = json_dict['calories']
    menu_url = json_dict['menuUrl']

    print nb_items
    print calories
    print menu_url

    with open('data.json') as data_file:
        data = json.load(data_file)

    return json.dumps(data)


if __name__ == '__main__':
    app.run()
