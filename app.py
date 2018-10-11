from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
import mysql.connector
from mysql.connector import errorcode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 

app = Flask(__name__)
app.debug = True

#config MysSQl
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = ''
#app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


connection =mysql.connector.connect(user='root',password= '',host= '127.0.0.1',database= 'flaskapp')

#init MQSQL
#mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def index():
       return "index"

@app.route('/articles')
def articles():
       return render_template('articles.html', articles = Articles )

@app.route('/article/<string:id>/')
def article(id):
       return render_template('article.html', id = id)


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
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s, %s, %s, %s)", (name,email,username,password))

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
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        

        if result > 0:
            #get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate,password):
                app.logger.info('PASSWORD MATCHED')
            else:
                app.logger.info('PASSWORD NOT MATCHED')    

        else:
            app.logger.info('NO USER')        


    return render_template('login.html')    


if __name__== '__main__':
    app.secret_key="secretkey123"
    app.run()



