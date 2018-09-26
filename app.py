from flask import Flask, render_template
from data import Articles

app = Flask(__name__)
app.debug = True


Articles = Articles()

@app.route('/')
def index():
       return "index"

@app.route('/articles')
def articles():
       return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
       return render_template('article.html', id = id)






if __name__== '__main__':
    app.run()
