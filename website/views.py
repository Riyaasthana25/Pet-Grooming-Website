from flask import Blueprint, render_template, flash, redirect, request, jsonify, session
from .models import Product, Cart, Order, Booking, Bookdetails
from flask_login import login_required, current_user
from . import db
# from intasend import APIService
from .forms import SlotBookingForm, PetForm, AddressForm, PaymentForm
from datetime import datetime


date1 = None
time_slot1 = None



views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_b32d1851-5572-488c-a7cf-1c0a841e4829'

API_TOKEN = 'ISSecretKey_test_8819513e-0f1c-459a-a5ba-0fcdc766bf2f'


@views.route('/')
def home():
    home_page = True
    items = Product.query.filter_by(flash_sale=True)
    products = Product.query.all()

    return render_template('home.html', items=items,products=products, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [], home_page=home_page)


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    action = request.args.get('action')
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            if action == 'add':
                flash(f' Quantity of { item_exists.product.product_name } has been updated')
                return redirect(request.referrer)
            elif action == 'order':
                flash(f' Quantity of { item_exists.product.product_name } has been updated')
                return redirect('/cart')
        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of { item_exists.product.product_name } not updated')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} has not been added to cart')
    if action == 'add':
        return redirect(request.referrer)
    elif action == 'order':
        return redirect('/cart')


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    len=0
    for item in cart:
        len+=1*item.quantity
        amount += item.product.current_price * item.quantity

    return render_template('cart.html',len=len, cart=cart, amount=amount, total=amount+0)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 0
        }

        return jsonify(data)


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':

        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 0,
            
        }

        return jsonify(data)


@views.route('/removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 0
        }

        return jsonify(data)


@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

    return render_template('search.html')

@views.route('/orders')
@login_required
def order():
    orders = Bookdetails.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)


# @views.route('/place-order')
# @login_required
# def place_order():
    
#     customer_cart = Cart.query.filter_by(customer_link=current_user.id)
#     # recent_booking = Booking.query.filter_by(customer_id=current_user.id).first()
#     # print("orders----->", recent_booking.date, recent_booking.time_slot)
#     if customer_cart:
#         try:
#             total = 0
#             for item in customer_cart:
#                 total += item.product.current_price * item.quantity

#             # service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
#             # create_order_response = service.collect.mpesa_stk_push(phone_number='8009119956', email=current_user.email,
#             #                                                        amount=total + 100, narrative='Purchase of goods')

#             for item in customer_cart:
#                 new_order = Order()
#                 new_order.quantity = item.quantity
#                 new_order.price = item.product.current_price
#                 new_order.status ='Pending'
#                 new_order.payment_id = 'ngyja13hyt67'
#                 # new_order.date =date
#                 # new_order.time_slot=time_slot

#                 new_order.product_link = item.product_link
#                 new_order.customer_link = item.customer_link

#                 db.session.add(new_order)
                

#                 product = Product.query.get(item.product_link)

#                 product.in_stock -= item.quantity

#                 db.session.delete(item)

#                 db.session.commit()

#             flash('Order Placed Successfully')

#             return redirect('/orders')
#         except Exception as e:
#             print(e)
#             flash('Order not placed')
#             return redirect('/')
#     else:
#         flash('Your cart is Empty')
#         return redirect('/')



@views.route('/book-grooming-meet', methods=['GET', 'POST'])
@login_required
def book_groomer():
    pet_form = PetForm()
    address_form = AddressForm()
    payment_form = PaymentForm()

    existing_booking = ["Empty"]
    print(existing_booking,"------->>",len(existing_booking))
    if request.method == 'POST':
        if pet_form.validate_on_submit() and 'submit_pet_form' in request.form:
                # Store pet form data in session
                session['pet_form_data'] = request.form.to_dict()
                return render_template('book_grooming_meet.html',  form=address_form, address_form=address_form,existing_booking=existing_booking)

        elif address_form.validate_on_submit() :
            if 'check_availability' in request.form:
                date = address_form.date.data
                time_slot = address_form.time_slot.data
                existing_booking = Booking.query.filter_by(date=date, time_slot=time_slot).all()
                print(existing_booking,"-------",len(existing_booking))
                if len(existing_booking) >= 3:
                    flash('Slot already booked. Please choose another slot.','warning')
                    return render_template('book_grooming_meet.html',  form=address_form, address_form=address_form,existing_booking=existing_booking)
                else:
                    flash('Slot is available. Please click on Continue.','success')
                    return render_template('book_grooming_meet.html',  form=address_form, address_form=address_form,existing_booking=existing_booking)
                
                
                return render_template('book_grooming_meet.html',  form=address_form, address_form=address_form,existing_booking=existing_booking)
                
                
                    # flash('Slot Available')
            elif 'submit_address_form' in request.form:
                session['address_form_data'] = request.form.to_dict()
                return render_template('book_grooming_meet.html',  form=payment_form, payment_form=payment_form,existing_booking=existing_booking)
        
        elif payment_form.validate_on_submit():
            if payment_form.payment_option.data == 'COD':
                customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
                pet_form_data = session.pop('pet_form_data')
                address_form_data = session.pop('address_form_data')
                # print("this is name:------->", address_form_data['date'])
                if customer_cart:
                    try:
                        total = 0
                        for item in customer_cart:
                            total += item.product.current_price * item.quantity

                        # service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
                        # create_order_response = service.collect.mpesa_stk_push(phone_number='8009119956', email=current_user.email,
                        #                                                       amount=total + 100, narrative='Purchase of goods')

                        
                        if (not pet_form_data) or (not address_form_data) :
                            flash('Pet form data missing. Please fill out the pet form first.', 'error')
                            return redirect('/book-grooming-meet')
                        for item in customer_cart:

                            new_order = Bookdetails()
                            new_order.pet_type=pet_form_data['pet_type']
                            new_order.breed=pet_form_data['breed']
                            new_order.gender=pet_form_data['gender']
                            new_order.size=pet_form_data['size']
                            new_order.aggression=pet_form_data['aggression']
                            new_order.vaccinated=pet_form_data['vaccinated']
                            new_order.age=pet_form_data['age']
                            new_order.name=address_form_data['name']
                            new_order.mobile_number=address_form_data['mobile_number']
                            new_order.pincode=address_form_data['pincode']
                            new_order.locality=address_form_data['locality']
                            new_order.address=address_form_data['address']
                            new_order.city=address_form_data['city']
                            new_order.state=address_form_data['state']
                            new_order.landmark=address_form_data['landmark']
                            new_order.alternate_mobile_number=address_form_data['alternate_mobile_number']
                            date_str=address_form_data['date']
                            new_order.date = datetime.strptime(date_str, '%Y-%m-%d').date()
                            new_order.time_slot=address_form_data['time_slot']
                            
                            
                            new_order.quantity = item.quantity
                            new_order.price = total
                            new_order.status = 'Booking Confirm'
                            new_order.payment_id = "Cash on Delivery"
                            

                            new_order.product_link = item.product_link
                            new_order.customer_link = item.customer_link

                            db.session.add(new_order)
                            db.session.delete(item)

                            # product = Product.query.get(item.product_link)

                            # product.in_stock -= item.quantity
                            
                            date = datetime.strptime(address_form_data['date'], '%Y-%m-%d').date()
                            time_slot = address_form_data['time_slot']
                            existing_booking = Booking.query.filter_by(date=date, time_slot=time_slot).all()
                            if len(existing_booking) < 3:
                                # Create a new booking if it doesn't exist
                                new_booking = Booking(date=date, time_slot=time_slot)
                                db.session.add(new_booking)
                                print("booking is done on--->>", date ,"and", time_slot)

                            db.session.commit()

    
                        flash('Order Placed Successfully')
                        return redirect('/orders')
                    except Exception as e:
                        print("this isexception",e)
                        db.session.rollback()
                        flash('Order not placed')
                        return redirect('/')
                else:
                    flash('Your cart is Empty')
                    return redirect('/')
                
                
    return render_template('book_grooming_meet.html',  form=pet_form, pet_form=pet_form, existing_booking=existing_booking)

@views.route('/order-details/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_details(order_id):
    order = Bookdetails.query.get(order_id)
    return render_template('order_details.html',order=order)

@views.route('/cancel-order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Bookdetails.query.get(order_id)
    if order:
        # Update order status to 'Canceled'
        order.status = 'Canceled'
        try:
            db.session.commit()
            flash('Successfully cancel order')
            return render_template('order_details.html',order=order)
        except Exception as e:
            print(e)
            flash('Failed to cancel order')
            return render_template('order_details.html',order=order)
    else:
        return render_template('404.html')

    