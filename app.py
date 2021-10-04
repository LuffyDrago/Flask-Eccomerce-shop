# html ,css, jvascript,python, jinja2 
from flask import *
import pymysql
from werkzeug.utils import secure_filename
import os

app = Flask(__name__) #flask oject takes name of application
# create a secret key used in encrypting the sessions
app.secret_key = "Atws@#$%&19*^*54ERW@$^OX1MZU"
UPLOAD_FOLDER = "static/img"
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Routing
@app.route('/')
def home():
    conn = pymysql.connect("localhost", "root", "", "shoe_db")
    cursor = conn.cursor()
    cursor.execute("select * from category")

    if cursor.rowcount < 1:
        return render_template('home.html', msg="No Products")
    else:
        rows = cursor.fetchall()
        return render_template('home.html', rows=rows)
    
@app.route('/admin')
def admin():
    if 'key' in session and session['role'] =='admin':
        return render_template('admin.html')
    else:
        return redirect("/login")

@app.route('/login', methods=['POST', 'GET'])
def login():
     if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # hash the password

        # we first connect to localhost and gelato_db
        conn = pymysql.connect("localhost", "root", "", "shoe_db")

        # insert the records into the users tables
        cursor = conn.cursor()
        cursor.execute("select * from users where email = %s and password=%s", (email, password))

        if cursor.rowcount == 1:
             # take me to a different route and create a session
            session['key'] = email
            row = cursor.fetchone()
            session['role']= row[2] 
                    #    print((row[2]))
            if row[2] =='user':        
                from flask import redirect
                #after successfull login, we create user session and redirect the user to /checkout
                return redirect('/mycart')
            elif row[2] ==  'admin':
                 from flask import redirect
                 return redirect('/admin')

            else:
                 from flask import redirect
                 return redirect('/login')


        else:
            return render_template('login.html', msg="Login Failed")

     else:
        return render_template('login.html')





@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

         # we first connect to localhost and soko_db
        conn = pymysql.connect("localhost","root","","shoe_db")

         # insert the records into the users tables
        cursor =  conn.cursor()
        cursor.execute("insert into users(email,password) values (%s,%s)", (email,password))
        conn.commit()
        return render_template('signup.html', msg= "Record Saved Succesfully")

    else:

         return render_template('signup.html')


@app.route('/contact')
def contact():
    return render_template('contactus.html')



# @app.route('/products')
# def products():
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     cursor.execute("select * from products")

#     if cursor.rowcount < 1:
#         return render_template('products.html', msg="No Products")
#     else:
#         rows = cursor.fetchall()
#         #return render_template('products.html', msg=rows)
#         return render_template('products.html',rows=rows)

# # This routes reads products based on id
# @app.route('/purchase/<id>')
# def purchase(id):
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     # execute the query using the cursor
#     cursor.execute("select * from products where product_id = %s", (id))
#     # check if no records were found
#     if cursor.rowcount < 1:
#         return render_template('purchase.html', msg="This Product does not exist")
#     else:
#         # return all rows found
#         rows = cursor.fetchall()
#         return render_template('purchase.html', rows=rows)

# # /all products/
# @app.route('/products')
# def products():
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     cursor.execute("select * from category")

#     if cursor.rowcount < 1:
#         return render_template('productsall.html', msg="No Products")
#     else:
#         rows = cursor.fetchall()
#         #return render_template('products.html', msg=rows)
#         return render_template('productsall.html',rows=rows)

# # /all prodcts

@app.route('/addproducts')
def addproducts():
     if 'key' in session and session['role'] =='admin':
        conn = pymysql.connect("localhost", "root", "", "shoe_db")
        cursor = conn.cursor()
        cursor.execute("select * from category")

        if cursor.rowcount < 1:
            return render_template('addproducts.html', msg="No Products")
        else:
            rows = cursor.fetchall()
            #return render_template('products.html', msg=rows)
            return render_template('addproducts.html',rows=rows)
     else:
        return redirect('/login')
# /adding category
@app.route('/addcategory')
def addcategory():
     if 'key' in session and session['role'] =='admin':
        conn = pymysql.connect("localhost", "root", "", "shoe_db")
        cursor = conn.cursor()
        cursor.execute("select * from category")

        if cursor.rowcount < 1:
            return render_template('addcategory.html', msg="No Products")
        else:
            rows = cursor.fetchall()
            #return render_template('products.html', msg=rows)
            return render_template('addcategory.html',rows=rows)
     else:
        return redirect('/login')
        # ADDING STUFF TO THE DATABASE
@app.route('/addproductstodb' , methods=['POST','GET'])
def addproductstodb():
    if request.method == 'POST':
        category = request.form['categoty_id']
        name = request.form['name']
        cost = request.form['cost']
        quantity = request.form['qtty']
        description = request.form['description']
        image = request.files['image']
        myFilename = secure_filename(image.filename)
         # we first connect to localhost and soko_db
        conn = pymysql.connect("localhost","root","","shoe_db")

         # insert the records into the users tables
        cursor =  conn.cursor()
        cursor.execute("insert into allproducts(category_id,name,cost,qtty,description,image) values (%s,%s,%s,%s,%s,%s)", (category, name,cost, quantity,description, myFilename ))
        conn.commit()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], myFilename))
        return redirect('addproducts')

    else:

         return redirect('addproducts')

# ADDING CATEGORY
@app.route('/addcategorytodb' , methods=['POST','GET'])
def addcategorytodb():
    if request.method == 'POST':
  
        name = request.form['name']
        
         # we first connect to localhost and soko_db
        conn = pymysql.connect("localhost","root","","shoe_db")

         # insert the records into the users tables
        cursor =  conn.cursor()
        cursor.execute("insert into category(name) values (%s)", (name ))
        conn.commit()
        return redirect('addcategory')

    else:

         return redirect('addcategory')

# products 
@app.route('/products')
def products():
    id = request.args.get('id')
    conn = pymysql.connect("localhost", "root", "", "shoe_db")
    cursor = conn.cursor()
    cursor.execute("select * from allproducts where category_id =" + id) 

    if cursor.rowcount < 1:
        return render_template('products.html', msg="No Products")
    else:
        rows = cursor.fetchall()
        #return render_template('products.html', msg=rows)
        return render_template('products.html',rows=rows)

# This routes reads products based on id
@app.route('/purchase/<id>')
def purchase(id):
    conn = pymysql.connect("localhost", "root", "", "shoe_db")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from allproducts where product_id = %s", (id))
    # check if no records were found
    if cursor.rowcount < 1:
        return render_template('purchase.html', msg="This Product does not exist")
    else:
        # return all rows found
        rows = cursor.fetchall()
        return render_template('purchase.html', rows=rows)


# /changes in DATABASE/
# @app.route('/products1')
# def products1():
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     cursor.execute("select * from products1")

#     if cursor.rowcount < 1:
#         return render_template('products1.html', msg="No Products")
#     else:
#         rows = cursor.fetchall()
#         #return render_template('products.html', msg=rows)
#         return render_template('products1.html',rows=rows)

# @app.route('/purchase1/<id>')
# def purchase1(id):
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     # execute the query using the cursor
#     cursor.execute("select * from products1 where product_id = %s", (id))
#     # check if no records were found
#     if cursor.rowcount < 1:
#         return render_template('purchase1.html', msg="This Product does not exist")
#     else:
#         # return all rows found
#         rows = cursor.fetchall()
#         return render_template('purchase1.html', rows=rows)


# @app.route('/products2')
# def products2():
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     cursor.execute("select * from products2")

#     if cursor.rowcount < 1:
#         return render_template('products2.html', msg="No Products")
#     else:
#         rows = cursor.fetchall()
#         #return render_template('products.html', msg=rows)
#         return render_template('products2.html',rows=rows)

# @app.route('/purchase2/<id>')
# def purchase2(id):
#     conn = pymysql.connect("localhost", "root", "", "shoe_db")
#     cursor = conn.cursor()
#     # execute the query using the cursor
#     cursor.execute("select * from products2 where product_id = %s", (id))
#     # check if no records were found
#     if cursor.rowcount < 1:
#         return render_template('purchase2.html', msg="This Product does not exist")
#     else:
#         # return all rows found
#         rows = cursor.fetchall()
#         return render_template('purchase2.html', rows=rows)



## THE ROUTE IS NOT NEEDED THE LOGOUT WAS REDIRECTED
# this route, users will need to login to access it
# @app.route('/checkout')
# def checkout():
#    if 'key' in session:
#             logged_in = session['key']
#             return render_template('checkout.html')

#    else:
#         from flask import redirect
#         return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('key',None)
    with sqlite3.connect('cart.db') as con:
        cursor = con.cursor()
        cursor.execute("delete  from items")
    from flask import redirect
    return redirect('/login')


# checkout   logout   login   checkout  logout checkout
# Creating shopping cart, flask,

# Option 1: Use JS  - Localhost
# Option 2: MySQL - database
# Option SQLite3

# build a simple cart with sqlite
from flask import redirect, url_for
# build a simple cart with sqlite
import sqlite3
con = sqlite3.connect('cart1.db')
con.execute('create table if not exists items(id INT, name TEXT, cost INT, qtty INT, total INT, email VARCHAR)')
@app.route('/cart', methods=['POST','GET'])
def cart():
    if 'key' in session and session['role'] =='user':
        if request.method == 'POST':
            id = request.form['id']
            name = request.form['name']
            cost = float(request.form['cost'])
            qtty = float(request.form['qtty'])
            total  = cost * qtty
            email = session["key"]



            with sqlite3.connect('cart1.db') as con:
                cursor = con.cursor()
                cursor.execute("insert into items(id,name,cost,qtty,total,email) values(?,?,?,?,?,?)",
                                (id,name,cost,qtty,total,email))
                con.commit()
                flash("Added To CART","success")


                return redirect(url_for('purchase', id=id))
        else:
            return redirect('products')
            #   return redirect('products1')
            #       return redirect('products2')
    else:
        return redirect("/login")
@app.route('/mycart')
def mycart():
    if 'key' in session and session['role'] =='user':
            with sqlite3.connect('cart1.db') as con:
                cursor = con.cursor()
                email = session["key"]
                cursor.execute("select * from items WHERE email =?",(email,))

                if cursor.rowcount==0:
                    return render_template('mycart.html', msg = "Your Basket is Empty")
                else:
                    rows = cursor.fetchall()

                # get totals
                    total_sum =0
                    for row in rows:
                        total_sum = total_sum + row[4]
                    return render_template('mycart.html', rows = rows, total_sum = total_sum)
    else:
             return redirect("/login")            

# Clear from sqlite
@app.route('/empty')
def empty():
    if 'key' in session and session['role'] =='user':
            with sqlite3.connect('cart1.db') as con:
                cursor = con.cursor()
                email = session["key"]
                cursor.execute("delete  from items WHERE email =?",(email,))
                return redirect('/mycart')
    else:
             return redirect("/login") 
        

#Consumer Key 	i5xrV6CFaW82A4DNMmrfoEiJXbI2wQvJ
#Consumer Secret 	NzJSsIe6TQ3ZGsH8 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa_payment/<total_amount>', methods = ['POST','GET'])
def mpesa_payment(total_amount):
        if 'key' in session:
                if request.method == 'POST':
                    phone = str(request.form['phone'])
                    amount = str(request.form['amount'])
                    #  itemss here
                    #GENERATING THE ACCESS TOKEN
                    consumer_key = "i5xrV6CFaW82A4DNMmrfoEiJXbI2wQvJ"
                    consumer_secret = "NzJSsIe6TQ3ZGsH8"

                    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
                    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

                    data = r.json()
                    access_token = "Bearer" + ' ' + data['access_token']

                    #  GETTING THE PASSWORD
                    timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
                    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
                    business_short_code = "174379"
                    data = business_short_code + passkey + timestamp
                    encoded = base64.b64encode(data.encode())
                    password = encoded.decode('utf-8')


                    # BODY OR PAYLOAD
                    payload = {
                        "BusinessShortCode": "174379",
                        "Password": "{}".format(password),
                        "Timestamp": "{}".format(timestamp),
                        "TransactionType": "CustomerPayBillOnline",
                        "Amount": "1",  # use 1 when testing
                        "PartyA": phone,  # change to your number
                        "PartyB": "174379",
                        "PhoneNumber": phone,
                        "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                        "AccountReference": "account",
                        "TransactionDesc": "account"
                    }

                    # POPULAING THE HTTP HEADER
                    headers = {
                        "Authorization": access_token,
                        "Content-Type": "application/json"
                    }

                    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

                    response = requests.post(url, json=payload, headers=headers)
                    print (response.text)
                    return render_template('mpesa_payment.html', msg = 'Please Complete Payment in Your Phone')
                else:
                    return render_template('mpesa_payment.html', total_amount=total_amount)
                    #return render_template('mpesa_payment.html', msg = 'Please Complete Payment in Your Phone')
                #else:
                    # return render_template('mpesa_payment.html', total_amount=total_amount)

               


        else:
             return redirect('/login')

















if __name__ == '__main__':
     app.debug = True
     app.run()