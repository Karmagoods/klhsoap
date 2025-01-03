from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key for sessions (use a secure key in production)
app.secret_key = 'your_secure_random_secret_key'

# Sample product data (this can be replaced with a database)
products = {
    'olive': {'name': 'Olive Soap', 'price': 90, 'description': 'Nourishing olive oil for soft, healthy skin.'},
    'honey': {'name': 'Honey & Almond Milk Soap', 'price': 90, 'description': 'Sweet and gentle care for delicate skin.'},
    'rose': {'name': 'Rose Soap', 'price': 90, 'description': 'Elegance and beauty in every use.'},
    'lavender': {'name': 'Lavender Soap', 'price': 90, 'description': 'Relaxing lavender scent for a calming experience.'},
    'orange': {'name': 'Orange with Jasmine Soap', 'price': 90, 'description': 'Bright and cheerful with a floral touch.'},
    'rosemary': {'name': 'Rosemary Soap', 'price': 90, 'description': 'Refreshing rosemary for invigorating skincare.'},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products_page():
    return render_template('products.html', products=products)  # Pass the 'products' dictionary here

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    product = products.get(product_id)
    if product:
        cart = session['cart']
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'name': product['name'], 'price': product['price'], 'quantity': 1}
        session['cart'] = cart
    else:
        return "Product not found", 404

    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/update_quantity/<product_id>', methods=['POST'])
def update_quantity(product_id):
    action = request.form['action']
    cart = session.get('cart', {})

    if product_id in cart:
        if action == 'increase':
            cart[product_id]['quantity'] += 1
        elif action == 'decrease' and cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_item/<product_id>', methods=['POST'])
def remove_item(product_id):
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    message = "This is a demo site. No payments will be processed."
    return render_template('checkout.html', message=message)

@app.route('/about')
def about():
    return render_template('about.html')  # Ensure the about.html file exists in the templates folder

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Ensure the contact.html file exists in the templates folder

if __name__ == '__main__':
    app.run(debug=True)
