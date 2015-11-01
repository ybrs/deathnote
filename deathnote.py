from flask import abort
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient()


@app.route('/new/', methods=['GET'])
def new():
    db = client['death']
    offset = int(request.args.get('offset', 0))
    pipeline = [{'$group': {'_id': '$name', 'count': {'$sum': 1}, 'datetime': {'$last': '$datetime'}}},
                {'$sort': {'datetime': -1}},
                {'$skip': offset},
                {'$limit': 20}
                ]
    deaths = db.posts.aggregate(pipeline)
    deaths = list(deaths)
    if not deaths and offset:
        abort(404)
    return render_template('index.html',
                           deaths=deaths,
                           kind='new',
                           offset=offset+20)

@app.route('/', methods=['GET', 'POST'])
def index():
    db = client['death']
    offset = int(request.args.get('offset', 0))
    if request.method == 'GET':
        pipeline = [{'$group': {'_id': '$name', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}},
                    {'$skip': offset},
                    {'$limit': 20}]
        deaths = db.posts.aggregate(pipeline)
        deaths = list(deaths)
        if not deaths and offset:
            abort(404)
        return render_template('index.html',
                               deaths=deaths,
                               kind='top',
                               offset=offset+20)

    else:
        data = request.json
        name = data.get('text')
        if name:
            post = db.posts.find({'name': name,
                                  'ip': request.remote_addr})
            post = list(post)
            if not post:
                if len(name) < 25:
                    db.posts.insert({'name': name,
                                     'ip': request.remote_addr,
                                     'datetime': datetime.now()})
        return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
