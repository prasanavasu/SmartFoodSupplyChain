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
from flask import Flask, request, jsonify, current_app, make_response, session, render_template, send_file
import sqlite3
from flask_cors import CORS, cross_origin
from numpy.compat import basestring

app = Flask(__name__)
cors = CORS(app)

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
    return render_template('index.html')


@app.route('/customer_login')
def customer_login():
    return render_template('customer_login.html')


@app.route('/supplier_login')
def supplier_login():
    return render_template('supplier_login.html')


@app.route('/distributor_login')
def distributor_login():
    return render_template('distributor_login.html')


@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('customer_dashboard.html')


@app.route('/supplier_dashboard')
def supplier_dashboard():
    return render_template('supplier_dashboard.html')


@app.route('/distributor_dashboard')
def distributor_dashboard():
    return render_template('distributor_dashboard.html')


@app.route('/incoming_requests')
def incoming_requests():
    return render_template('incoming_requests.html')


@app.route('/outgoing_requests')
def outgoing_requests():
    return render_template('outgoing_requests.html')


@app.route('/api/login', methods=['POST'])
@cross_origin()
@crossdomain(origin='*')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        db = sqlite3.connect('inventory.db')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            # storing for later access
            # session['username'] = username

            # Close the cursor and commit changes
            cursor.close()
            db.close()
            return jsonify({'message': 'Login successful', 'user_type': user[3]})
        else:
            # Close the cursor and commit changes
            cursor.close()
            db.close()
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



def get_products():
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()

    # Fetch product data from the database
    cursor.execute('SELECT * FROM Stock')
    products = cursor.fetchall()

    # Close the database connection
    connection.close()

    if products:
        username = 'suhil'
        # Convert the products list to a dictionary format
        product_data = [{'product_name': product[1], 'quantity': product[7]} for product in products]
        return product_data , username
    else:
        return False

@app.route('/api/products/', methods=['GET'])
def get_product_items():
    products = get_products()
    if products:
        return jsonify({'username': products[1], 'products': products[0]})
    return jsonify({'error': 'Product not found'}), 404



@app.route('/api/checkproductstock', methods=['GET'])
def check_products_stock():
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()

    # Fetch products from the database
    cursor.execute('SELECT * FROM stock')
    products = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Apply business rules algorithm
    priority_to_threshold = {
        1: 1000,
        2: 800,
        3: 500
    }

    priority_of_product = {
        'Rice': 2000,
        'Lentils': 1000,
        'Sugar': 2000,
        'Oil': 500,
        'Milk': 500,
        'Tomatoes': 800,
        'Onions': 800,
        'Whole Grains': 1000,
        'Soy': 1000
    }

    products_with_status = []

    for product in products:

        product_name = product[1]
        priority = priority_of_product.get(product_name, 0)

        product_dict = {
            'product_id': product[0],
            'product_name': product[1],
            'priority': priority,
            'quantity': product[7]
        }

        # Determine stock status based on threshold
        #  threshold = priority_to_threshold.get(priority, 0)
        if product[7] >= priority:
            product_status = 'In Stock'
        else:
            product_status = 'Out of Stock'

        product_dict['status'] = product_status
        products_with_status.append(product_dict)

    return jsonify({'products': products_with_status})


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


# Sample data for products and hubs
products_data = [
    {"product_name": "Product A", "quantity": 10, "status": "In Stock", "hub": "Hub A"},
    {"product_name": "Product A", "quantity": 0, "status": "Out of Stock", "hub": "Hub B"},
    {"product_name": "Product B", "quantity": 5, "status": "In Stock", "hub": "Hub A"},
    {"product_name": "Product B", "quantity": 8, "status": "In Stock", "hub": "Hub B"},
    # ... add more product data here
]


@app.route('/api/find_top_hubs_for_out_of_stock_product', methods=['POST'])
def find_top_hubs_for_out_of_stock_product():
    data = request.json

    product_name = data.get('product_name')
    hubs_with_same_product = {}

    for entry in products_data:
        if entry['product_name'] == product_name and entry['status'] == 'In Stock':
            if entry['hub'] in hubs_with_same_product:
                hubs_with_same_product[entry['hub']] += entry['quantity']
            else:
                hubs_with_same_product[entry['hub']] = entry['quantity']

    sorted_hubs = sorted(hubs_with_same_product.items(), key=lambda x: x[1], reverse=True)[:3]

    result = [{"hub": hub, "total_quantity": quantity} for hub, quantity in sorted_hubs]

    return jsonify({"top_hubs": result})


# Sample data for incoming and outgoing requests
requests_data = [
    {"type": "Incoming", "product": "Product A", "hub": "Hub A"},
    {"type": "Outgoing", "product": "Product B", "hub": "Hub B"},
    # ... add more request data here
]


@app.route('/api/requests', methods=['GET'])
def get_requests():
    return jsonify({"requests": requests_data})


if __name__ == '__main__':
    app.run(debug=True)
