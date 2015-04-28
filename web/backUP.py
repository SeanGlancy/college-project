from flask import Flask, render_template, redirect,url_for, request, session, flash, jsonify
from functools import wraps
from MyUtils import UseDatabase

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
    scan= request.args.get('text', "", type=str) # scan result is stored in scan
    with UseDatabase(lottoApp.config) as cursor:
        SQL = """select status from ticketDetails where barcode = %s"""
        cursor.execute(SQL,(scan,))
        the_data = cursor.fetchall()

    return  jsonify(suc=the_data)


@lottoApp.route('/home')
@login_required
def home():
	return render_template('home.html')


@lottoApp.route('/welcome')
def welcome():
	return render_template('welcome.html')

@lottoApp.route('/applogin',methods=['GET','POST'])
def applogin():
    id= request.args.get('id', "unknown", type=str)
    passw= request.args.get('pass', "unknown", type=str)
    if id == '':
        result= 'Id required'
        return  jsonify(suc=result)
    elif passw == '':
        result= 'password required'
        return  jsonify(suc=result)


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
