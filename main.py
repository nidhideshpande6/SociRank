#------------------------------------------------database---------------------------------------------------------------
import sqlite3
import os
conn = sqlite3.connect('topic_prediction_database')
cur = conn.cursor()
#import syss
import requests


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('treebank')
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
#------------------------------------------------database---------------------------------------------------------------
"""import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


import nltk

nltk.download('wordnet')
from nltk.corpus import wordnet as wn


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


from nltk.stem.wordnet import WordNetLemmatizer


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)"""

from flask import Flask,render_template, url_for,request, flash, redirect, session
app = Flask(__name__)
app.config['SECRET_KEY'] = '881e69e15e7a528830975467b9d87a98'
#-------------------------------------home_page-------------------------------------------------------------------------

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

#-------------------------------------home_page-------------------------------------------------------------------------

#-------------------------------------about_page-------------------------------------------------------------------------
@app.route("/about")
def about():
   return render_template('about.html')
#-------------------------------------about_page-------------------------------------------------------------------------

#-------------------------------------user_login_page-------------------------------------------------------------------------
@app.route('/user_login',methods = ['POST', 'GET'])
def user_login():
   conn = sqlite3.connect('topic_prediction_database')
   cur = conn.cursor()
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['psw']
      print('asd')
      count = cur.execute('SELECT * FROM user WHERE email = "%s" AND password = "%s"' % (email, password))
      print(count)
      #conn.commit()
      #cur.close()
      l = len(cur.fetchall())
      if l > 0:
         flash( f'Successfully Logged in' )
         return render_template('user_account.html')
      else:
         print('hello')
         flash( f'Invalid Email and Password!' )
   return render_template('user_login.html')

# -------------------------------------user_login_page-----------------------------------------------------------------

@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    print(request.method)
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        print(file1,file2)
        file1 = file1.filename
        fp = open(file1)
        data1 = fp.read()
        fp.close()

        file2 = file2.filename
        tokens1 = nltk.word_tokenize(data1)
        tagged1 = nltk.pos_tag(tokens1)
        topic1 = []
        for i in tagged1:
            print(i)
            if i[1] == 'NNP' or i[1] == 'NN':
                topic1.append(i[0])
        topic1 = list(set(topic1))
        print(topic1)

        fp = open(file2)
        data2 = fp.read()
        fp.close()
        tokens2 = nltk.word_tokenize(data2)
        tagged2 = nltk.pos_tag(tokens2)
        topic2 = []
        for i in tagged2:
            print(i)
            if i[1] == 'NNP' or i[1] == 'NN':
                topic2.append(i[0])
        topic2 = list(set(topic2))
        print(topic2)
        l = min(len(topic1),len(topic2))
        a = []
        for i in range(l):
            a.append([topic1[i],topic2[i]])
        return render_template('analyse.html',q = a)
    return render_template('search.html')
# -----------------------------------predict_page-----------------------------------------------------------------

@app.route('/predict', methods=['POST', 'GET'])
def predict():

    country = request.form['country']
    catogery = request.form['catogery']

    print(country,catogery)
    if request.method == 'POST':
        url = ('https://newsapi.org/v2/top-headlines?'
               'country={}&'.format(country)+'apiKey=878a2fc5700b4cd2a9eeec5115f7712b')
        # url = 'https://newsapi.org/v2/everything?q=keyword&apiKey=878a2fc5700b4cd2a9eeec5115f7712b'
        response = requests.get(url)

        data1 = response.json()['articles']
        title = []
        for i in data1:
            print(i['title'])
            title.append(i['title'])
        #data = response.category
        #print(data)

        tokens1 = nltk.word_tokenize(str(title))
        tagged1 = nltk.pos_tag(tokens1)
        #print(tagged1)
        topic2 = []
        for i in tagged1:
            #print(i)
            if i[1] == 'NNP' or i[0] != 'None' or i[0] != 'https' or '[' not in i[0] or ',' not in i[0] :# or i[1] == 'NN':
                topic2.append(i[0])
        #for i in data1:
        #    print(i['title'])
        #print(topic2)
        #print(max(topic2))
        #topic2.remove(max(topic2))
        removetable = str.maketrans('', '', r',:@#%}][,…’{$}+')
        #topic2  = [s.translate(removetable) for s in topic2]
        topic2 = list(set(topic2))
        #print("topic = ", topic2)
        #print(data1)
        return render_template('search.html',title=title,cont=country)
    return render_template('user_account.html')
#------------------------------------------------predict_page-----------------------------------------------------------------

# ------------------------------------search_page-----------------------------------------------------------------
@app.route('/search')
def search():
   return render_template('search.html')
# ------------------------------------search_page-----------------------------------------------------------------

# -------------------------------------user_register_page---------------------------------------------------------
@ app.route('/user_register', methods=['POST', 'GET'])
def user_register():
   conn = sqlite3.connect('topic_prediction_database')
   cur = conn.cursor()
   if request.method == 'POST':
      name = request.form['uname']
      email = request.form['email']
      password = request.form['psw']
      gender = request.form['gender']
      age = request.form['age']

      cur.execute("insert into user(name,email,password,gender,age) values ('%s','%s','%s','%s','%s')" % (name, email, password, gender, age))
      conn.commit()
      # cur.close()
      print('data inserted')
      return redirect(url_for('user_login'))
   return render_template('user_register.html')
# -------------------------------------user_register_page-------------------------------------------------------------------------

# -------------------------------------user_account_page-------------------------------------------------------------------------
@app.route('/user_account',methods = ['POST', 'GET'])
def user_account():
   return render_template('user_account.html')
# -------------------------------------user_account_page-------------------------------------------------------------------------

# -------------------------------------user_logout_page-------------------------------------------------------------------------
@app.route("/logout")
def logout():
   session['logged_in'] = False
   return home()

@app.route("/logoutd",methods = ['POST','GET'])
def logoutd():
   return home()# -------------------------------------user_logout_page-------------------------------------------------------------------------

if __name__ == '__main__':
   app.secret_key = os.urandom(12)
   app.run(debug=True)

