from . import db
from flask_login import UserMixin
from datetime import datetime
from wtforms import TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash
from pytz import timezone

IST = timezone('Asia/Kolkata')  # Indian Standard Time


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    mobile_number=db.Column(db.Integer)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    cart_items = db.relationship('Cart', backref=db.backref('customer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('customer', lazy=True))
    bookdetails = db.relationship('Bookdetails', backref=db.backref('customer', lazy=True))

    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __str__(self):
        return '<Customer %r>' % Customer.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_type = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Integer, nullable=False)
    previous_price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    # description = db.Column(db.Text) 
    # description = db.Column(ARRAY(db.String), nullable=True)
    # description = db.Column(db.String(1500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now(IST))

    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))
    bookdetails = db.relationship('Bookdetails', backref=db.backref('product', lazy=True))


    def __str__(self):
        return '<Product %r>' % self.product_name


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # customer product

    def __str__(self):
        return '<Cart %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)
   
    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    # booking = db.relationship('Booking', backref=db.backref('order', lazy=True))
    # booking = db.Column(db.Integer, db.ForeignKey('booking.id'))  

    # customer
    def __str__(self):
        return '<Order %r>' % self.id

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Booking(id={self.id}, date={self.date}, time_slot={self.time_slot})"


class Bookdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    aggression = db.Column(db.String(10), nullable=False)
    vaccinated = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    locality = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    landmark = db.Column(db.String(100))
    alternate_mobile_number = db.Column(db.String(15))
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now(IST))

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return '<Bookdetails %r>' % self.id