from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.types import DateTime
from app import db

class Rating(db.Model):
    id = Column(Integer, primary_key=True)
    rating = Column(String(50))

class Roles(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    

class Users(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(100))
    password = Column(String(100))
    role = Column(String(100), ForeignKey('roles.id'))
    rating = Column(String(100), ForeignKey('rating.id'))
    created_date = Column(DateTime())
    modified_date = Column(DateTime())
    location = Column(String(50))
  

class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_date = Column(DateTime())
    modified_date = Column(DateTime())

class Stock(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    category_Id =  Column(String(100), ForeignKey('category.id'))
    unit_price = Column(String(50))
    quantity = Column(String(50))
    created_date = Column(DateTime())
    modified_date = Column(DateTime())
    location = Column(String(50))

class Orders(db.Model):
    id = Column(Integer, primary_key=True)
    stock_id =  Column(String(100), ForeignKey('stock.id'))
    category_Id =  Column(String(100), ForeignKey('category.id'))
    quantity = Column(String(50))
    order_date = Column(DateTime())
    status = Column(String(100))
