from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
#from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
import mysql.connector
from mysql.connector import errorcode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 
from functools import wraps
import psycopg2
import os



app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("config.Production")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.Testing")
else:
    app.config.from_object("config.Development")








#config MysSQl
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = ''
#app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#mysql connection
#connection =mysql.connector.connect(user='root',password= '',host= '127.0.0.1',database= 'flaskapp')

#postgress connection
connection =psycopg2.connect(user='rfmkwvcfumreqf',password= '8e71f7cc2f00e02739616de00ddc69132fa72d75e82cd2c94185befe81ef433f',host= 'ec2-174-129-227-128.compute-1.amazonaws.com', 
database= 'd3gacb20iaqb6g', port='5432')


#init MQSQL
#mysql = MySQL(app)

#Articles = Articles()

@app.route('/')
def index():
       return render_template('home.html')

@app.route('/articles')
def articles():
       
    #creare cursor
    cur = connection.cursor()
    #get articles
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    #print(articles)
    return render_template('articles.html', articles = articles)
    

    

    #close connection
    cur.close()    

@app.route('/article/<string:id>/')
def article(id):
    #creare cursor
    cur = connection.cursor()
    #get articles
    cur.execute("SELECT * FROM articles where id = %s",[id])
    articles = cur.fetchone()
    
    return render_template('article.html', articles = articles)


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message ="Passwords do not match")
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name =  form.name.data
        email= form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))


        #Create cursor
        #connection = mysql.connect()
        cur = connection.cursor()


        

        #execute query
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s, %s, %s, %s)", (name,email,username,password));

        #commit to DB
        connection.commit()


        #close connection
        cur.close()

        flash("You are now registered and can now log in", 'success')


        return redirect(url_for('login'))
    return render_template('register.html', form = form) 

#User Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #create a cursor
        cur = connection.cursor()
        


        #get user by username
        data= cur.execute("SELECT * FROM users WHERE username = %s", [username])
        data = cur.fetchone()[3]
        
            #compare passwords
        if sha256_crypt.verify(password_candidate,data):
            session['logged_in'] = True
            session['username'] = username

            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid logins'   
            return render_template('login.html', error=error) 

             


    return render_template('login.html') 

#check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please login','danger')
            return redirect(url_for('login'))   
    return wrap     


#logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return redirect(url_for('login'))


#dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    #creare cursor
    cur = connection.cursor()

    #get articles
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    results = cur.rowcount

    if results > 0:
        #print(articles)
        return render_template('dashboard.html', articles = articles)
    else:
        msg = "No articles found"    
        return render_template('dashboard.html', msg = msg)


    
    
    

    

    #close connection
    cur.close()    


    

#Article form class
class ArticleForm(Form):
    title = StringField('Title', [validators.length(min=1, max=200)])
    body = TextAreaField('Body', [validators.length(min=30)])
    
#add article route
@app.route('/add_article', methods=['POST', 'GET']) 
@is_logged_in   
def add_articles():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate:
        title = form.title.data
        body = form.body.data


        #create cursor
        cur = connection.cursor()

        #execute
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)",(title,body,session['username']))

        #commit to database
        connection.commit()

        #close connection
        cur.close()

        flash("Articles created", 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form = form)  



#Edit article route
@app.route('/edit_article/<string:id>', methods=['POST', 'GET']) 
@is_logged_in   
def edit_articles(id):


      #get form
      form = ArticleForm(request.form)

      #create cursor
      cur = connection.cursor()

      result = cur.execute("SELECT * FROM articles WHERE id = %s" , [id]) 
      article = cur.fetchone() 

     

      #populate article form fields
      form.title.data = article[1]
      form.body.data = article[2]
    
      if request.method == 'POST' and form.validate:
            title = request.form['title']
            body = request.form['body']


            #create cursor
            cur = connection.cursor()

            #execute
            cur.execute("UPDATE articles SET title = %s, body = %s WHERE id = %s", (title,body,id))

            #commit to database
            connection.commit()

            #close connection
            cur.close()

            flash("Articles Updated", 'success')

            return redirect(url_for('dashboard'))

      return render_template('edit_article.html', form = form) 


  #Delete article
@app.route("/delete_article/<string:id>", methods=['POST'])
@is_logged_in
def delete_article(id):

      #create cursor
      cur = connection.cursor()

      #execute
      cur.execute("DELETE FROM articles WHERE id = %s", [id])

      connection.commit()

            #close connection
      cur.close()

      flash("Articles Deleted", 'success')

      return redirect(url_for('dashboard'))

  



if __name__== '__main__':
   # app.secret_key="secretkey123"
    app.run()



