from flask import Blueprint, render_template, flash, send_from_directory, redirect, request
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, Bookdetails
from . import db


admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = ShopItemsForm()
     
        if form.validate_on_submit():
            pet_type = form.pet_type.data
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            discount = form.discount.data
            flash_sale = form.flash_sale.data
            
            descriptions = [description for description in form.descriptions.data if description is not None]
            # descriptions = [description.data for description in form.descriptions.entries if description.data]
            description_text = '\n'.join(descriptions) if descriptions else ''

            file = form.product_picture.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)
            # print("--->>>>><<<<<<-----",form.descriptions.data)
            new_shop_item = Product(
                    pet_type = pet_type,
                    product_name=product_name,
                    current_price=current_price,
                    previous_price=previous_price,
                    in_stock=in_stock,
                    discount=discount,
                    flash_sale=flash_sale,
                    description=description_text,
                    product_picture=file_path
                )
            # print("----->>>>",description_text)

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added Successfully')
                # print('Product Added')
                return render_template('add_shop_items.html', form=form)
            except Exception as e:
                print("this is error here---->",e)
                flash('Product Not Added!!')

        return render_template('add_shop_items.html', form=form)

    return render_template('404.html')


@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemsForm()

        item_to_update = Product.query.get(item_id)
        form.pet_type.render_kw = {'value': item_to_update.pet_type}
        form.product_name.render_kw = {'value': item_to_update.product_name}
        form.previous_price.render_kw = {'value': item_to_update.previous_price}
        form.descriptions.render_kw = {'value': item_to_update.description}
        form.current_price.render_kw = {'value': item_to_update.current_price}
        form.in_stock.render_kw = {'value': item_to_update.in_stock}
        form.discount.render_kw = {'value': item_to_update.discount}
        form.flash_sale.render_kw = {'value': item_to_update.flash_sale}
        form.product_picture.render_kw = {'value': item_to_update.product_picture}
        # print(item_to_update.description)
        if form.validate_on_submit():
            pet_type = form.pet_type.data
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            discount = form.discount.data
            flash_sale = form.flash_sale.data

            descriptions = [description for description in form.descriptions.data if description is not None]
            # descriptions = [description.data for description in form.descriptions.entries if description.data]
            description_text = '\n'.join(descriptions) if descriptions else ''

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=item_id).update(dict(pet_type = pet_type,
                                                                product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                description=description_text,
                                                                product_picture=file_path))

                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Upadted')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not Upated', e)
                flash('Item Not Updated!!!')

        return render_template('update_item.html', form=form)
    return render_template('404.html')


@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect('/shop-items')
        except Exception as e:
            # print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect('/shop-items')

    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Bookdetails.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        # orders = Bookdetails.query.all()
        form = OrderForm()

        order = Bookdetails.query.get(order_id)
        # print({{ order.product.product_picture }}")
        # order = Bookdetails.query.filter_by(id=order_id).first()
        # print(order.name)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} not updated')
                return redirect('/view-orders')

        return render_template('order_update.html',order=order, form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')