import sqlite3

import bcrypt
from flask import Flask

app = Flask(__name__)
db = sqlite3.connect('inventory.db')
cursor = db.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        CreatedDate DATE,
        ModifiedDate DATE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stock (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        Description TEXT,
        Category_Id INTEGER,
        Unit_Price INTEGER,
        CreatedDate DATE,
        ModifiedDate DATE,
        FOREIGN KEY (Category_Id) REFERENCES Category (Id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Supplier (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        Address TEXT,
        Phone INTEGER,
        Rating_Id INTEGER,
        CreatedDate DATE,
        ModifiedDate DATE,
        FOREIGN KEY (Rating_Id) REFERENCES Ratings (Id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ratings (
        Id INTEGER PRIMARY KEY,
        Rating INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Status (
        Id INTEGER PRIMARY KEY,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        Id INTEGER PRIMARY KEY,
        Stock_Id INTEGER,
        Category_Id INTEGER,
        Quantity INTEGER,
        Order_date DATE,
        Status_Id INTEGER,
        FOREIGN KEY (Stock_Id) REFERENCES Stock (Id),
        FOREIGN KEY (Category_Id) REFERENCES Category (Id),
        FOREIGN KEY (Status_Id) REFERENCES Status (Id)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER PRIMARY KEY,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        UserType TEXT NOT NULL,
        CreatedDate DATE NULL,
        ModifiedDate DATE NULL
    )
''')

for i in range(3):
    if i == 1:
        name = 'sai'
        role = 'supplier'
    if i == 2:
        name = 'prasanna'
        role = 'distributor'
    if i == 0:
        name = 'suhil'
        role = 'customer'
    hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute('''
        INSERT INTO Users (Username, Password, UserType, CreatedDate, ModifiedDate)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, hashed_password, role, '2023-08-17', '2023-08-17'))

    # Repeat similar code for other user types

db.commit()
