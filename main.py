import requests
from lxml import html
import io
from pyvi import ViTokenizer
from string import punctuation

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)


f = io.open("stopword.txt", mode="r", encoding='utf8')
list_stopword = [line.rstrip() for line in f]
print(list_stopword)
def tran(sentence):
    data = {
        'cp1': sentence,
        'mode': 1,
        'rpage': 1
    }
    r = requests.post('http://www.easyvn.com/tiengviet/compose.php', data=data)

    my_str = r.text
    lxml_mysite = html.fromstring(my_str)
    data = lxml_mysite.xpath('//font[@id ="WORKFONT"]/a/text()')

    line = ' '.join(data)
    return line

def process(str):
    str = tran(str)
    str = str.lower()
    str = ''.join(c for c in str if c not in punctuation)

    tach = ViTokenizer.tokenize(str)
    filtered_words = [word.replace("_", " ") for word in tach.split(" ") if word not in list_stopword]

    return [str, filtered_words]

class getAns(Resource):
    def post(self):
        content = request.get_json()
        print(content)
        result = process(content['message'])
        print('ans = ' + str(result))
        return {
            'trans': result[0],
            'split': result[1]
        }


api.add_resource(getAns, '/trans')
tack = tran("thoi tiet cua ngay mai")
print(tack)
if __name__ == '__main__':
    run = app.run(port=5000, debug=False)
