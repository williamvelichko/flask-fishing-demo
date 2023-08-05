from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Sample product data (you can replace this with your actual product data)
products = [
    {"id": 1, "name": "Fishing Rod", "price": 50.0, 'img': "https://www.meltontackle.com/media/catalog/product/d/a/daiwa-free-swimmer-spinning-reel-10000-side_1.jpg"},
    {"id": 2, "name": "Fishing Reel", "price": 30.0,  'img': "https://www.meltontackle.com/media/catalog/product/d/a/daiwa-free-swimmer-spinning-reel-10000-side_1.jpg"},
    {"id": 3, "name": "Fishing Lures", "price": 10.0,  'img': "https://www.meltontackle.com/media/catalog/product/d/a/daiwa-free-swimmer-spinning-reel-10000-side_1.jpg"},

]
selected_products = []

@app.route('/')
def index():
    return render_template('index.html', products=products)


@app.route('/item/<int:product_id>', methods=['GET', 'POST'])
def item(product_id):
    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        return render_template('404.html', 404)

    if request.method == 'POST':
        selected_products.append(product)
        return redirect(url_for('checkout'))

    return render_template('singleItem.html', product=product)


@app.route('/add_to_checkout', methods=['POST'])
def add_to_checkout():
    product_id = int(request.form['product_id'])
    product = next((p for p in products if p['id'] == product_id), None)


    if not product:
        return render_template('404.html', 404)

    selected_products.append(product)

    return redirect(url_for('checkout'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():


    # Get the selected product IDs from the form
    selected_ids = request.form.getlist('product')
    total_price = sum(product['price'] for product in selected_products)

    # Find the selected products and calculate the total price
    for product in products:
        if str(product['id']) in selected_ids:
            selected_products.append(product)
            total_price += product['price']



    return render_template('checkout.html', products=selected_products, total_price=total_price)



if __name__ == '__main__':
    app.run(debug=True)