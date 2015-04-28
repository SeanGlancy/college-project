from flask import Flask, render_template, redirect,url_for, request, session, flash, jsonify
from functools import wraps
import re
import random
import requests
from MyUtils import UseDatabase


lottoApp = Flask(__name__)

lottoApp.secret_key = "ultimate secret_key of doom"

def varExtractor(data):     # to convert tuple to string
        List = list(data)
        Val = str(List[0])
        return Val

#check ticket
@lottoApp.route('/')
def checkTicket():
    #count=0
    scan= request.args.get('text', "", type=str) # scan result is stored in scan

    with UseDatabase(lottoApp.config) as cursor:
        SQL = """select status from ticketDetails where barcode = %s"""
        cursor.execute(SQL,(scan,))
        the_data = cursor.fetchall()

    status=varExtractor(the_data)

    count=5
    result="Ticket result is "+ status +" with "+ str(count)
    return  jsonify(suc=result)

# ////////////////////////////to return number of number matched////////////////
#    if the_data == "winner":
#        with UseDatabase(lottoApp.config) as cursor:
#            SQL = """select date from ticketDetails where barcode = %s"""
#            cursor.execute(SQL,(scan,))
#            ticketDate = cursor.fetchall()

#        with UseDatabase(lottoApp.config) as cursor:
#            SQL = """select number1,number2,number3,number4,number5,number6 from ticketDetails where barcode = %s"""
#            cursor.execute(SQL,(scan,))
#            resultA = cursor.fetchall()

#        with UseDatabase(lottoApp.config) as cursor:
#            SQL = """select number1,number2,number3,number4,number5,number6 from lottoResults where date = %s"""
#            cursor.execute(SQL,(ticketDate,))
#            resultB = cursor.fetchall()

#            seta = set(resultA)
#            setb = set(resultB)

#            match = seta.intersection(setb)


#sent from the app
@lottoApp.route('/applogin',methods=['GET','POST'])
def applogin():
    id= request.args.get('userid', "", type=str)
    passw= request.args.get('passwd', "", type=str)

    if id == "":
        result= 'Id required'
        return  jsonify(suc=result)
    elif passw == '':
        result= 'password required'
        return  jsonify(suc=result)
    isValid=[]
    with UseDatabase(lottoApp.config) as cursor:
        SQL = """select username from userDetails where username = %s AND passwd = %s"""
        cursor.execute(SQL,(id,passw,))
        isValid = cursor.fetchall()

    if isValid ==None:
        result= 'Logged in'
        return  jsonify(suc=result)



#/////////////////////////////////////////////////////////////////////////LOGIN///////////////////////////////////////////////////////////////////////////////////////////////////////


@lottoApp.route('/login')
def login():
    return render_template('login.html')


@lottoApp.route('/processLogin', methods=['POST'])
def process():
    allGood=True
    userid = request.form['userid']
    passwd = request.form['passwd']
        # Check that a login and password arrived from the FORM.
    if len( userid ) < 4:
        flash("Sorry. userID must be greater than 4 characters. Try again")
        allGood=False
    if passwd == '':
        flash("Sorry. Password cant be blank. Try again")
        allGood=False


    if allGood:
        isValid=[]
        with UseDatabase(lottoApp.config) as cursor:
            SQL = """select username from userDetails where username = %s AND passwd = %s"""
            cursor.execute(SQL,(userid,passwd,))
            isValid = cursor.fetchall()

        if isValid == []:
            flash("Login successful")
            return render_template('welcome.html')
        else:
            pass

    else:
        return redirect(url_for("login"))

#/////////////////////////////////////////////////////////////////////////PAGE LOAD///////////////////////////////////////////////////////////////////////////////////////////////////////
@lottoApp.route('/welcome')
def welcome():
	return render_template('welcome.html')

@lottoApp.route('/admin')
def admin():
    return render_template('adminLogin.html')

@lottoApp.route('/adminLogin')
def adminLogin():
    allGood=True
    userid = request.form['userid']
    passwd = request.form['passwd']

    if passwd == '':
        flash("Sorry. Password cant be blank. Try again")
        allGood=False
    if userid == '':
        flash("Sorry. id cant be blank. Try again")
        allGood=False

    if allGood:
        if passwd == 'admin' and userid =='admin':
            return render_template('admin.html')
        else:
            flash('invalid credentials')
            pass
    else:
        return render_template('adminLogin.html')

#/////////////////////////////////////////////////////////////////////////register///////////////////////////////////////////////////////////////////////////////////////////////////////
@lottoApp.route('/register')
def register():
    return render_template('reg.html')

@lottoApp.route('/processReg',methods=['POST'])
def processReg():

    allGood=True
    userid = request.form['userid']
    passwd = request.form['passwd']
    email= request.form['email']
    passwd2 = request.form['passwd2']

    if re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])', passwd) is None:
        flash("Password must have 1 upper case letter, 1 lower case letter and a number")
        allGood=False

    for x in userid:#change to assci to check for spaces
        if ord(x) == 32:
            flash("UserName cannot have a space")
            allGood=False

        if email == '':
            flash("Email required")
            allGood=False

        if passwd == "": # check if password is blank
            flash("Password required")
            allGood=False

        if len( userid) < 4 :
            flash("userName must be greater than 4 characters")
            allGood=False

        if passwd != passwd2:
            flash("Passwords do not match")
            allGood=False

        if allGood:
            isValid=[]#check if in table already
            with UseDatabase(lottoApp.config) as cursor:
                SQL = """select * from userDetails where userName = %s"""
                cursor.execute(SQL,(userid,))
                isValid = cursor.fetchall()

            if isValid == []:
                with UseDatabase(lottoApp.config) as cursor:
                    SQL ="""insert into userDetails(username,passwd,email) values(%s,%s,%s)"""
                    cursor.execute(SQL,(userid,passwd,email,))

            send(email,userid)
            flash("Please confirm email, check Email")
            return render_template('login.html')

        else:
            flash("UserName already in use")
            return redirect(url_for("register"))

#///////////////////////////////////////////////////////send email///////////////////////////////
def send(email,user):

    return requests.post(
        "https://api.mailgun.net/v3/sandboxd75f310b94c2491587fa79cd828e52a9.mailgun.org/messages",
        auth=("api", "key-3c04794b5c9ebc35fb6e981b8e078833"),
        data={"from": "Registration Team <seanglancy@ymail.com>",
              "to": email,
              "subject": "Confirm Registration",
              "html": """<html>

Dear """+ user +"""

Please confirm your account by visiting the link:
http://c00156721.pythonanywhere.com/verify?type="""+user+"""
<br>
The Registration Team

                        </html>"""})
def createReset(email,userid):

    num = random.randrange(1, 100000)
    num=str(num)

    with UseDatabase(lottoApp.config) as cursor:
        SQL ="""insert into userDetails(randomKey) values(%s) where username=%s"""
        cursor.execute(SQL,(num,userid))


    sendReset(email,userid)
def sendReset(email,user):

    return requests.post(
        "https://api.mailgun.net/v3/sandboxd75f310b94c2491587fa79cd828e52a9.mailgun.org/messages",
        auth=("api", "key-3c04794b5c9ebc35fb6e981b8e078833"),
        data={"from": "Registration Team <seanglancy@ymail.com>",
              "to": email,
              "subject": "Confirm Registration",
              "html": """<html>

Dear """+ user +"""

To reset Password go to:
http://c00156721.pythonanywhere.com/verify?type="""+user+"""
<br>
The Registration Team

                        </html>"""})

@lottoApp.route('/verify',methods=['GET'])
def verify():
    name =self.request.get("type")
    with UseDatabase(lottoApp.config) as cursor:
        SQL = """select * from userDetails where userName = %s"""
        cursor.execute(SQL,(name,))
        isValid = cursor.fetchall()


#////////////////////////////////////////resest password/////////////////////////
@lottoApp.route('/resetPass')
def resest():
    return render_template('reset.html')

@lottoApp.route('/resetProcess',methods=['POST'])
def resestProcess():

    userid = request.form['userid']
    email = request.form['email']
    allGood=True
    if userid == '':
        flash("userID required")
        allGood=False

    if email == "":
        flash("Email required")
        allGood=False
    isValid=[]

    if allGood:
        with UseDatabase(lottoApp.config) as cursor:
            SQL = """select * from userDetails where userName = %s AND email = %s """
            cursor.execute(SQL,(userid,email,))
            isValid = cursor.fetchall()
    else:
        return render_template('reset.html')


    if isValid == None:
        flash('reset email sent')
        createReset(email,userid)
    else:
        flash("userID not found")
        return render_template('reset.html')







if __name__ == '__main__':
    lottoApp.run(debug=True)
