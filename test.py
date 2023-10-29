import os
import pickle
from flask import Flask, request, jsonify, url_for, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import numpy as np
import pandas as pd
import jwt
import datetime
import secrets

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key=secret_key

#load the model
regmodel = pickle.load(open('model.pkl', 'rb'))
scalar=pickle.load(open('scaling.pkl','rb'))

#Database connection
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'user.db')
app.config['SCERET_KEY']=secret_key
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(128), nullable=False)

#creating home page
@app.route('/')
def index():
    return render_template('index.html')





#creating contact page with get, post method and also with jwt token
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method =='POST':
        data = request.get_json()
        # Add logic to store user data in the database
        return jsonify({'message': 'User created successfully!'})
    else:
        return render_template('contact.html')
    




#creating signup page with get, post method and also with jwt token
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        data = request.get_json()
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Check if user already exists by email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists!'})
        else:
            hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')
            # Create a new user
            new_user = User(username=username, name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            # Generate a token
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'message': 'User created successfully!', 'token': token.decode('UTF-8')})
    else:
        return render_template('signup.html')






#creating login page with get, post method and also with jwt token
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and Bcrypt().check_password_hash(user.password, password):
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return render_template('user.html', username=username, name=user.name, email=user.email, token=token.decode('UTF-8'))
            
        else:
            return render_template('login.html', message='Incorrect username/password combination!')
    return render_template('login.html')






#User index page route(if user is logged in then only he can access this page)
@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('predict.html')
    # if 'user' in session:
    #     username = session['user']
    #     user = User.query.filter_by(username=username).first()
    #     if request.method=='POST':
    #         data=request.json['data']
    #         print(data)
    #         print(np.array(list(data.values())).reshape(1,-1))
    #         new_data = scalar.transform(np.array(list(data.values())).reshape(1,-1))
    #         output = regmodel.predict(new_data)
    #         print(output[0])
    #         return jsonify(output[0])
    #     return render_template('user.html', username=username, name=user.name, email=user.email)
    # else:
    #     flash('You are not logged in')
    #     return redirect(url_for('login'))    





#creating /predict route with get, post method and also with jwt token
@app.route('/predict_api', methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output = regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])





@app.route('/predict', methods=['GET','POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scalar.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=regmodel.predict(final_input)[0]
    
    if output<0:
        return render_template("predict.html",prediction_text="The House price should be less than a millon: {}".format(output)+" lakhs in dollars")
    elif int(output) >99:
        return render_template("predict.html",prediction_text="The House price should be around: {}".format(int(output))+" crore in dollars")
    else:
        return render_template("predict.html",prediction_text="The House price should be around: {}".format(int(output))+" lakh in dollars")





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    