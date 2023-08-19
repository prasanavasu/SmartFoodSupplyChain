import base64
import io
from datetime import timedelta
from functools import update_wrapper

import bcrypt
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.use('Agg')
from flask import Flask, request, jsonify, current_app, make_response, session, render_template, send_file,redirect
import sqlite3
from flask_cors import CORS, cross_origin
from numpy.compat import basestring

from app import app,db
from app.models import *
from datetime import datetime


# Simulated inventory data (you would use a database in reality)
inventory = {
    'product_1': 1100,
    'product_2': 1150,
    'product_3': 1510,
    'product_4': 1520,
    'product_5': 1523,
    'product_6': 1502,
    'product_7': 1500,
    'product_8': 1510,
    'product_9': 1590,
    'product_10': 9150,
    'product_11': 10150

}


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """

        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon():
    return app.send_static_file('apple-touch-icon-precomposed.png')


@app.route('/')
def index():
    return render_template('index.html',title='Smart Food Supply Chain Management System',home='active')

@app.route('/add/role')
def role():
    role = ['supplier','distributor','customer']
    for i in role:
        if not Roles.query.filter_by(name=i).first():
            role = Roles(name=i)
            db.session.add(role)
            db.session.commit()
    return "Role added"

@app.route('/users')
def users():
    role = Roles.query.all()
    return render_template('add_user.html',title='Users',role=role)

@app.route('/category')
def category():
    return render_template('category.html',title='category')

@app.route('/product')
def products():
    category = Category.query.all()
    return render_template('products.html',title='Products',category=category)

@app.route('/add/users', methods=['POST'])
def add_users():
    phone = request.form.get('phone')
    password = request.form.get('password')
    email = request.form.get('email')
    name = request.form.get('name')
    role = request.form.get('role')
    location = request.form.get('location')
    role_id = Roles.query.filter_by(name=role).first()
    message = 'Invalid Role'
    if role_id:
        message = 'Already Registered'
        if not Users.query.filter_by(phone=phone).first():
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = Users(location=location,name=name,email=email,phone=phone,password=hashed_password,role=role_id.id,created_date=datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect('/users')
    return jsonify({'error': message}), 400

@app.route('/add/product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    unit_price = request.form.get('unit_price')
    category = request.form.get('category')
    location = request.form.get('location')
    category_Id = Category.query.filter_by(name=category).first()
    message = 'Invalid Category'
    if category_Id:
        message = 'Already Registered'
        if not Stock.query.filter_by(name=name).first():
            user = Stock(name=name,unit_price=unit_price,quantity=quantity,description=description,category_Id=category_Id.id,created_date=datetime.now(),location=location)
            db.session.add(user)
            db.session.commit()
            return redirect('/product')
    return jsonify({'error': message}), 400


@app.route('/add/category', methods=['POST'])
def add_category():
    name = request.form.get('name')
    message = 'Already Registered'
    if not Category.query.filter_by(name=name).first():
        user = Category(name=name,created_date=datetime.now())
        db.session.add(user)
        db.session.commit()
        return redirect('/category')
    return jsonify({'error': message}), 400

def check_products_stock(pk,value):
    priority_of_product = {
        'Rice': 2000,
        'Lentils': 1000,
        'Sugar': 2000,
        'Oil': 500,
        'Milk': 500,
        'Tomatoes': 800,
        'Onions': 800,
        'Whole Grains': 1000,
        'Soy': 1000,
        'Bread': 500
    }
    if int(pk) >= priority_of_product[value]:
        product_status = True
    else:
        product_status = False
    return product_status

@app.route('/<pk>')
def customer_login(pk=None):

    if pk == 'customer' :

        html_template = 'customer_dashboard.html' if (session.get('role') == 'customer') else 'customer_login.html'
        title = 'Customer Dashboard' if (session.get('role') == 'distributor') else 'Customer Login'
        products = Stock.query.all()
        return render_template(html_template,title=title,customer='active',products=products)

    elif pk == 'supplier':
        products = Stock.query.all()
        html_template = 'supplier_dashboard.html' if (session.get('role') == 'supplier') else 'supplier_login.html'
        title = 'Supplier Dashboard' if (session.get('role') == 'supplier') else 'Supplier Login'
        return render_template(html_template,title=title,supplier='active',products=products,stocks=check_products_stock)

    if pk == 'distributor':
        html_template = 'distributor_dashboard.html' if (session.get('role') == 'distributor') else 'distributor_login.html'
        title = 'Distributor Dashboard' if (session.get('role') == 'distributor') else 'Distributor Login'
        return render_template(html_template,title=title,distributor='active')

    else:
        return redirect('/')
    


@app.route('/logout')
def logout():
    if session.get('name'):
        del session['name']
    if session.get('role'):
        del session['role']
    return redirect('/')

@app.route('/api/login', methods=['POST'])
@cross_origin()
@crossdomain(origin='*')
def login():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    if phone and password:
        user = Users.query.filter_by(phone=phone).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # storing for later access
            session['name'] = user.name
            session['hub'] = user.location
            
            # Close the cursor and commit changes
            role = Roles.query.filter_by(id=user.role).first()
            session['role'] =  role.name
            return jsonify({'message': 'Login successful', 'user_type': role.name})
        else:
            # Close the cursor and commit changes

            return jsonify({'error': 'Invalid credentials'}), 401

    else:
        return jsonify({'error': 'Invalid request data'}), 400


# API route to get product availability
# Inventory Management
@app.route('/api/products/<product_id>', methods=['GET'])
def get_product_availability(product_id):
    if product_id in inventory:
        return jsonify({'product_id': product_id, 'available_quantity': inventory[product_id]})
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/api/products/', methods=['GET'])
def get_products():
    products = Stock.query.all()



    if products:
        username = 'suhil'
        # Convert the products list to a dictionary format
        product_data = [{'product_name': product.name, 'quantity': product.quantity} for product in products]
        return jsonify({'username': username, 'products': product_data})
    else:
        return jsonify({'error': 'Product not found'}), 404


# @app.route('/supplier_dashboard', methods=['GET'])
# def supplier_dashboard():
#     # Fetch products from the database
#     products = check_products_stock()
#
#     # Categorize products into In Stock and Out of Stock
#     in_stock_products = []
#     out_of_stock_products = []
#     for product in products:
#         if product['status'] == 'In Stock':
#             in_stock_products.append(product)
#         else:
#             out_of_stock_products.append(product)
#
#     return render_template('supplier_dashboard.html',
#                            in_stock_products=in_stock_products,
#                            out_of_stock_products=out_of_stock_products)

@app.route('/api/send_request', methods=['POST'])
def send_request():
    data = request.json

    # Extract product and hub from the request data
    product = data.get('product')
    hub = data.get('hub')

    # Implement the logic to send the request to the specified hub
    # You can use external APIs or libraries to send the request

    return jsonify({'message': 'Request sent successfully'})



@app.route('/api/visualizations/<visualization_id>', methods=['GET'])
def getTopSellingStock(visualization_id):
    # Top Selling Stock
    plt.switch_backend('agg')
    data = pd.read_csv('sales.csv')
    if visualization_id == 'getTopSellingStock':
        # Process the data to get the top selling stock
        # Example: Get the top 5 selling stocks
        top_selling = data.groupby('category')['quantity'].sum().nlargest(5)

        # Create a bar plot of the top selling stocks
        plt.figure(figsize=(10, 6))
        top_selling.plot(kind='bar')
        plt.xlabel('Stock')
        plt.ylabel('Total Quantity Sold')
        plt.title('Top Selling Stocks')

        # Save the plot to an in-memory buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close()

        # Return the image data as a response
        # return send_file(img_buffer, mimetype='image/png')

        # Return the image URL as JSON response
        return jsonify({"imageUrl": "data:image/png;base64," + base64.b64encode(img_buffer.read()).decode()})

    elif visualization_id == 'busiestHour':

        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['hour'] = data['timestamp'].dt.hour

        hourly_counts = data['hour'].value_counts()

        hourly_counts = hourly_counts.sort_index()

        plt.figure(figsize=(10, 6))
        plt.bar(hourly_counts.index, hourly_counts.values)
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Transactions')
        plt.title('Busiest Hour for Transactions')
        plt.xticks(range(24))
        plt.grid(axis='y')

        # Save the plot to an in-memory buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close()

        # Return the image URL as JSON response
        return jsonify({"imageUrl": "data:image/png;base64," + base64.b64encode(img_buffer.read()).decode()})

    else:
        return jsonify({'error': 'Visualization not found'}), 404

