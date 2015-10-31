from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.son import SON

app = Flask(__name__)
client = MongoClient()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = client['death']
    if request.method == 'GET':
        pipeline = [{'$group': {'_id': '$name', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}}]
        deaths = db.posts.aggregate(pipeline)
        return render_template('index.html', deaths=list(deaths))
    else:
        data = request.json
        name = data.get('text')
        if name:
            post = db.posts.find({'name': name, 'ip': request.remote_addr})
            post = list(post)
            if not post:
                if len(name) < 25:
                    db.posts.insert({'name': name, 'ip': request.remote_addr})
        return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
