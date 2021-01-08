##################################################################
##  SignupPage.py                                               ##
##  Signup Page V1.4  Build 291                                 ##
##                                                              ##
##  A simple Flask based application for signup.                ##
##                                                              ##
##  Copyright © 2017 iGolchin Foundation. All rights reserved.  ##
##################################################################

"""
This web application is licensed under GNU GENERAL PUBLIC LICENSE (GPL) for the good of web development
See ./LICENSE

For bug reporting and more information, please contact: BUG [at] iGolchin [dot] com
"""

#........................................

import os
import random
import string
import json
import hashlib
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash
from flask import make_response
from flask import abort
from flask_mail import Mail
from flask_mail import Message

#........................................

app = Flask(__name__)
app.secret_key='@edru9t&%53qibrz98j1a'
salt = "L2zREQqYn$6Q1dBht"

#........................................

letters = string.ascii_lowercase
letters = ''.join(random.choice(letters) for i in range(20))
# print(letters)
hashedCookie = hashlib.md5(letters.encode('utf-8'))

#........................................

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup/', methods=['POST'])
def signupAccount():
    ######## get Data ########
    session['name']=request.form['name']
    session['password']=request.form['password']
    session['mail']=request.form['mail']
    session['name'] = str.lower(session['name'])
    session['mail'] = str.lower(session['mail'])
    ######## Existing Check ########
    try:
        isExist = os.path.isfile('./JSON/%(nameFile)s.json' % {"nameFile": session['name']})

    except:
        print("bikhial")

    if (session['name'] !='') and (session['password']!='') and (session['mail'] != ''):
        if isExist:
            flash('This User exist')
            return redirect('/')
        else:

            ######## Saving Hashed Username && Hashed Password ########
            userName = session['name']
            hashedUsername = hashlib.sha1(userName.encode('utf-8'))

            data ={session['name']:session['password'] + salt}
            with open(os.path.join('./JSON/%(nameFile)s.json'%{"nameFile":hashedUsername.hexdigest()}), 'w') as jsn:
                json.dump(data, jsn,indent = 2)

            with open(os.path.join('./JSON/%(nameFile)s.json'%{"nameFile":hashedUsername.hexdigest()}), 'r') as jsn:
                passwd = json.load(jsn)
                for j in passwd:
                    i = j

            hashedPassword = hashlib.sha1(passwd[i].encode('utf-8'))

            data = {hashedUsername.hexdigest(): hashedPassword.hexdigest()}
            # print(data)
            with open(os.path.join('./JSON/%(nameFile)s.json'%{"nameFile":hashedUsername.hexdigest()}), 'w') as jsn:

                json.dump(data, jsn,indent = 2)

            ######## Saving Email ########

            emailData = {session['name']:session['mail']}
            with open(os.path.join('./email/%(nameFile)s.json'%{"nameFile":hashedUsername.hexdigest()}), 'w') as jsn:
                json.dump(emailData, jsn)

            ######## Success && Cookie saving ########

            redirectToIndex = redirect('/registerSuccess/')
            response = make_response(redirectToIndex)
            response.set_cookie(session['name'], value=hashedCookie.hexdigest())
            return response
    else:
        flash('Somthing went wrong, please try again!')
        return redirect('/')

@app.route('/signin/', methods=['POST'])
def checkPasswordAndName():
    session['name']=request.form['name']
    session['password']=request.form['password']
    session['name'] = str.lower(session['name'])
    userName = session['name']
    hashedUsername = hashlib.sha1(userName.encode('utf-8'))
    if (session['name'] !='') and (session['password']!=''):

        try:
            with open(os.path.join('./JSON/%(nameFile)s.json'%{"nameFile":hashedUsername.hexdigest()}), 'r') as jsn:
                data = json.load(jsn)

                for j in data:
                    i = j
        except:
            flash("Username or Passowrd is wrong!")
            return redirect('/')
        session['password'] = session['password'] + salt
        hashedPassword = hashlib.sha1(session['password'].encode('utf-8'))

        if hashedUsername.hexdigest() == i:
            if hashedPassword.hexdigest() == data[i]:

                ######## Success && Cookie saving ########

                redirectToIndex = redirect('/dashboard/')
                response = make_response(redirectToIndex)
                response.set_cookie(session['name'], value=hashedCookie.hexdigest())
                return response
            else:
                flash('Username or Passowrd is wrong!')
                return redirect('/')
        else:
            flash('Username or Passowrd is wrong!')
            return redirect('/')
    else:

        return redirect('/')

@app.route('/dashboard/',methods=['GET'])
def dashboardPage():

    ######## Checking Cookies ########

    flag = request.cookies.get(session['name'])
    if flag == hashedCookie.hexdigest():
        return render_template('dashboard.html')
    else:
        abort(403)

@app.route('/registerSuccess/',methods=['GET'])
def register():
    ######## Sending Welcome message ########
    mail = Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'www.igolchin@gmail.com'
    app.config['MAIL_PASSWORD'] = 'yhaqiixaachoemjn'

    msg = Message("Hello",
                  sender="www.igolchin@gmail.com",
                  recipients=[session['mail']],
                  body="Thank you for registring with our service")
    mail.send(msg)
    return 'Thanks For sign up in our service, Please check your email for more information  ' + session['name']


app.run(port=11000,debug=False)
