from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField,  TextAreaField, DateField, RadioField, FieldList
from wtforms.validators import DataRequired, length, NumberRange, Length, Regexp
from flask_wtf.file import FileField, FileRequired
from datetime import datetime


class SignUpForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), length(min=2)])
    email = EmailField('Email', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[
        DataRequired(),
        Length(min=10, max=10, message='Mobile number must be 10 digits'),
        Regexp('^[0-9]+$', message='Mobile number must contain only digits')
    ])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Sign-in')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')



class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = IntegerField('Current Price', validators=[DataRequired()])
    previous_price = IntegerField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    discount = IntegerField('Discount', validators=[DataRequired(), NumberRange(min=0)])
    pet_type = RadioField('Type of Your Pet', choices=[('Cat', 'Cat'), ('Dog', 'Dog')], validators=[DataRequired()])
    product_picture = FileField('Product Picture', validators=[DataRequired()])
    # description = TextAreaField('Description', validators=[DataRequired()])
    # descriptions = FieldList(StringField('Description'), min_entries=1)
    # descriptions = FieldList(StringField('Description'), min_entries=1)
    descriptions = FieldList(StringField('Description'))
    flash_sale = BooleanField('Flash Sale')
    # description = TextAreaField('Description', validators=[DataRequired()])

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')


class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('', '--select slot--'), ('Booking Confirm', 'Booking Confirm'),('Completed', 'Completed'), ('Canceled', 'Canceled')])
    update = SubmitField('Update')



class SlotBookingForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time_slot = SelectField('Time ', choices=[('', '--select slot--'),('09:00-11:00', '09:00-11:00'), ('11:00-01:00', '11:00-01:00'), ('01:00-03:00', '01:00-03:00'), ('03:00-05:00', '03:00-05:00'), ('05:00-07:00', '05:00-07:00')], validators=[DataRequired()])
    submit = SubmitField('Book Slot')


class PetForm(FlaskForm):
    pet_type = RadioField('Type of Your Pet', choices=[('Cat', 'Cat'), ('Dog', 'Dog')], validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    size = RadioField('Size of your Pet', choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], validators=[DataRequired()])
    aggression = RadioField('Aggressiveness', choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High')], validators=[DataRequired()])
    vaccinated = RadioField('Vaccinated', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    submit_pet_form = SubmitField('CONTINUE')

class AddressForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired()])
    locality = StringField('Locality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', default='Lucknow', validators=[DataRequired()])
    state = StringField('State', default='Uttar Pradesh', validators=[DataRequired()])
    landmark = StringField('Landmark')
    alternate_mobile_number = StringField('Alternate Mobile Number')
    date = DateField('Date Of Booking', validators=[DataRequired()], format='%Y-%m-%d')
    time_slot = SelectField('Time ', choices=[('', '--select slot--'),('09:00-11:00', '09:00-11:00'), ('11:00-01:00', '11:00-01:00'), ('01:00-03:00', '01:00-03:00'), ('03:00-05:00', '03:00-05:00'), ('05:00-07:00', '05:00-07:00')], validators=[DataRequired()])
    check_availability = SubmitField('Check Availability')
    submit_address_form = SubmitField('CONTINUE')

class PaymentForm(FlaskForm):
    # payment_option = RadioField('Payment Option', choices=[('COD', 'Cash on Delivery'), ('UPI', 'UPI')],
    #                             validators=[DataRequired()])
    payment_option = RadioField('Payment Option', choices=[('COD', 'Cash on Delivery')],
                                validators=[DataRequired()])
    submit_payment_form = SubmitField('Confirm Order')