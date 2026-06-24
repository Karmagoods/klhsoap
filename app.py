from flask import (
    Flask, render_template, request, redirect, 
    url_for, session, flash, get_flashed_messages
)
import os

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()   # Load .env file if exists

# ====================== CONFIG ======================
app.secret_key = os.environ.get('SECRET_KEY', 'your_secure_random_secret_key')  # ← Change in production!

# Sample product data (easily replaceable with database later)
products = {
    'olive': {
        'name': 'Olive Soap',
        'price': 90,
        'description': 'Nourishing olive oil for soft, healthy skin.',
        'image': 'images/olive.jpg'
    },
    'honey': {
        'name': 'Honey & Almond Milk Soap',
        'price': 90,
        'description': 'Sweet and gentle care for delicate skin.',
        'image': 'images/honey.jpg'
    },
    'rose': {
        'name': 'Rose Soap',
        'price': 90,
        'description': 'Elegance and beauty in every use.',
        'image': 'images/rose.jpg'
    },
    'lavender': {
        'name': 'Lavender Soap',
        'price': 90,
        'description': 'Relaxing lavender scent for a calming experience.',
        'image': 'images/lavender.jpg'
    },
    'orange': {
        'name': 'Orange with Jasmine Soap',
        'price': 90,
        'description': 'Bright and cheerful with a floral touch.',
        'image': 'images/orange.jpg'
    },
    'rosemary': {
        'name': 'Rosemary Soap',
        'price': 90,
        'description': 'Refreshing rosemary for invigorating skincare.',
        'image': 'images/rosemary.jpg'
    },
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def products_page():
    return render_template('products.html', products=products)


@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    product = products.get(product_id)
    if not product:
        flash("Product not found!", "error")
        return redirect(url_for('products_page'))

    cart = session['cart']

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'image': product['image']
        }

    session.modified = True  # Important when modifying mutable session objects
    flash(f"{product['name']} added to cart!", "success")
    
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    
    return render_template('cart.html', 
                         cart=cart_items, 
                         total=total)


@app.route('/update_quantity/<product_id>', methods=['POST'])
def update_quantity(product_id):
    action = request.form.get('action')
    cart = session.get('cart', {})

    if product_id in cart:
        if action == 'increase':
            cart[product_id]['quantity'] += 1
        elif action == 'decrease':
            if cart[product_id]['quantity'] > 1:
                cart[product_id]['quantity'] -= 1
            else:
                del cart[product_id]

    session.modified = True
    return redirect(url_for('cart'))


@app.route('/remove_item/<product_id>', methods=['POST'])
def remove_item(product_id):
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]
        flash("Item removed from cart.", "info")
    
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Cart cleared.", "info")
    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('cart'))
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    message = "This is a demo site. No payments will be processed."
    
    return render_template('checkout.html', 
                         cart=cart, 
                         total=total, 
                         message=message)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)   # ← Set to False in production