from flask import Flask, render_template, request
from query import search
from elasticsearch_dsl import Index

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def hello_world():
    # return "hello world"
    if request.method == 'POST':
        query = request.form['searchTerm']
        res = search(query)
        hits = res['hits']['hits']
        time = res['took']
        num_results = res['hits']['total']['value']

        return render_template('search_results.html', query=query, hits=hits, num_results=num_results, time=time)

    if request.method == 'GET':
        return render_template('index.html', init='True')


if __name__ == '__main__':
    app.run()
