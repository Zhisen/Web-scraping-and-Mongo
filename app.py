from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars_info

@app.route('/scrape')
def scrape():
    collection.drop()
    collection.insert_one(scrape_mars.scrape())
    return redirect('/', code = 302)


@app.route('/')
def home():
    info = collection.find_one()
    return render_template('index.html', info = info)






if __name__ == '__main__':
    app.run(debug=True)










