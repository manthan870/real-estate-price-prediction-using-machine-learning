import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import pickle
from flask import Flask, render_template, request, redirect, url_for ,flash ,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
import numpy as np
from flask_bcrypt import check_password_hash


#load the model
regmodel = pickle.load(open('model.pkl', 'rb'))
scalar=pickle.load(open('scaling.pkl','rb'))



app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_BINDS'] = {
#     'contact': 'sqlite:///contact.db'
# }

app.config['SECRET_KEY'] = 'c95e21ff72c64e17c5b92eab360d341ac58f2f9b0aed54ac' 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Create a User model to represent the user data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(80), nullable=False)
    c_email= db.Column(db.String(80), nullable=False)
    c_message = db.Column(db.String(120), nullable=False)
    c_date = db.Column(db.DateTime, default=datetime.utcnow)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        c_name = request.form.get('c_name')
        c_email = request.form.get('c_email')
        c_message = request.form.get('c_message')
        entry=Contact(c_name=c_name,c_email=c_email,c_message=c_message)
        db.session.add(entry)
        db.session.commit()
        flash("Your message has been sent. We'll get back to you shortly.", "success")
        
        # # send mail
        # mail="manthanchoudhary870@gmail.com"
        # subject="PropertyHub user query name=" +name
        # msg=MIMEMultipart()
        # body="Name: "+name +"\nMessage: "+message
        # msg['From']=email
        # msg['To']=mail
        # msg['Subject']=subject
        # msg.attach(MIMEText(body,'plain'))

        # with smtplib.SMTP('localhost',25) as server:
        #     server.sendmail(email,mail,msg.as_string())
        # return render_template('contact.html', mail_msg="Your message has been sent. We'll get back to you shortly.")
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['loginUsername']
        password = request.form['loginPassword']

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Password matches, user is authenticated
            flash("Login successful!", "success")
            session['user_id'] = user.id  
            session['user_name'] = user.name # Store user ID in session
            return redirect(url_for('user'))
        else:
            flash("Login failed. Please check your username and password.", "danger")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['signupUsername']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash("Username or email already exists. Please choose another one.", "danger")
        elif password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, name=name, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            session['user_name'] = name
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        else:
            flash("Password mismatch. Please check your password.", "danger")

    return render_template('signup.html')

@app.route('/user')
def user():
    user_name = session.get('user_name')
    if user_name:
        return render_template('user.html', user_name=user_name)
    else:
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user_info = {
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at
            }
            return render_template('dashboard.html', user_info=user_info, user=user)  # Pass user object
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                new_password = request.form['newPassword']
                user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('dashboard'))
    return render_template('change_password.html')






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
        output*100
        return render_template("user.html",prediction_text="The House price should be less than a lakhs: {}".format(output)+" thousands in dollars")
    elif int(output) >99:
        output/100
        return render_template("user.html",prediction_text="The House price should be around: {}".format(int(output))+" crore in dollars")
    else:
        return render_template("user.html",prediction_text="The House price should be around: {}".format(int(output))+" lakhs in dollars")




@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.pop('user_id', None)
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)
    