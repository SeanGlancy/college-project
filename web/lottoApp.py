from flask import Flask, render_template, redirect,url_for, request, session, flash, jsonify
from functools import wraps

lottoApp = Flask(__name__)

lottoApp.secret_key = "ultimate secret_key of doom"

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@lottoApp.route('/')
def checkTicket():
         a= request.args.get('text', "", type=str) # scan result is a
         result="hello"
         return  jsonify(suc=result)
	#connect to database
	#search for value in db

@lottoApp.route('/home')
@login_required
def home():
	return render_template('home.html')
     

@lottoApp.route('/welcome')
def welcome():
	return render_template('welcome.html')

@lottoApp.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session ['logged_in'] = True
			flash('You have logged in successfully, woooo')
			return redirect(url_for('home'))
	return render_template('login.html',error=error)

@lottoApp.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You have been logged out, bye')
	return redirect(url_for('welcome'))


if __name__ == '__main__':
	lottoApp.run(debug=True)
