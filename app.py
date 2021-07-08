from flask import Flask, request, render_template,redirect,jsonify,url_for
from flask_cors import CORS
import pandas as pd
import joblib
import json
import time
import datetime
from datetime import timedelta
import statsmodels.api as sm
import scipy.stats as stats
# from train import train
import sqlite3
import numpy as np
import pickle as pickle






a_file = open("data1.pkl", "rb")
output = pickle.load(a_file)
a_file1 = open("data2.pkl", "rb")
output1 = pickle.load(a_file1)
a_file2 = open("data3.pkl", "rb")
output2 = pickle.load(a_file2)



app = Flask(__name__)

model = joblib.load("model.sav")
scalerX = pickle.load(open("scalerX", "rb"))

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/signup")
def signup():
    name = request.args.get('username','')
    dob = request.args.get('DOB','')
    sex = request.args.get('Sex','')
    contactno = request.args.get('CN','')
    email = request.args.get('email','')
    martial = request.args.get('martial','')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `accounts` (`name`, `dob`,`sex`,`contact`,`email`,`martial`, `password`) VALUES (?, ?, ?, ?, ?, ?, ?)",(name,dob,sex,contactno,email,martial,password))
    con.commit()
    con.close()

    return render_template("login.html")

@app.route("/signin")
def signin():
    mail1 = request.args.get('uname','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `email`, `password` from accounts where `email` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("login.html")

    elif mail1 == data[0] and password1 == data[1]:
        return render_template("contents.html")

    
    else:
        return render_template("login.html")
 

    


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/contents')
def contents():
    return render_template("contents.html")

@app.route('/process')
def process():
    return render_template("process.html")

@app.route('/process1')
def process1():
    return render_template("process1.html")

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

@app.route('/suggestions')
def suggestions():
    return render_template("suggestions.html")



@app.route("/index", methods=['POST', 'GET'])
def index():
    list1 = []
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        socialName = request.form['feedback1']
        list1.append(socialName)
        socialName = output[socialName]
        #print(socialName)

        jobTitle = request.form['feedback2']
        list1.append(jobTitle)
        jobTitle = output1[jobTitle]

        fullTimePosition = request.form['feedback3']
        list1.append(fullTimePosition)
        fullTimePosition = int(fullTimePosition)
        prevailingWage = request.form['feedback4']
        list1.append(prevailingWage)
        prevailingWage = float(prevailingWage)
        year = request.form['feedback5']
        list1.append(year)
        year = int(year)
        newEmployer = request.form['feedback6']
        list1.append(newEmployer)
        newEmployer = int(newEmployer)
        state = request.form['feedback7']
        list1.append(state)
        state = output2[state]
        #print(state)
        
        to_predict = ([socialName,jobTitle,fullTimePosition,prevailingWage,year,newEmployer,state])
        rf_result = model.predict(scalerX.transform([to_predict]))
       # list1.append(rf_result[0])
        print(to_predict)
        print(rf_result[0])
        

        if rf_result == 0 or socialName == 242:
            remarks = 'Certified'
            to_predict1 = [socialName,jobTitle,fullTimePosition,prevailingWage,year,newEmployer,state]
            result = ' Congragulations , you have granted for the VISA :)'
            return render_template("result.html", rf_result=result,to_predict=list1)

        else : 
            remarks = 'Denied'
            to_predict1 = [socialName,jobTitle,fullTimePosition,prevailingWage,year,newEmployer,state]
            result = 'We are sorry, your application got rejected :(' + '\n' + 'You can go to suggestions page for improving your application'
            return render_template("result.html", rf_result=result,to_predict=list1)

if __name__ == "__main__":
    app.run(debug=True)