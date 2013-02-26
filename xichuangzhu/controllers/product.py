#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.product_model import Product

# page - shop
#--------------------------------------------------

# view
@app.route('/shop')
def shop():
	products = Product.get_products(12)
	return render_template('shop.html', products=products)

# page - single product
#--------------------------------------------------

# view
@app.route('/product/<int:product_id>')
def single_product(product_id):
	product = Product.get_product(product_id)
	return render_template('single_product.html', product=product)

# page - add product
#--------------------------------------------------

# view
@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
	if request.method == 'GET':
		return render_template('add_product.html')
	elif request.method == 'POST':
		product      = request.form['product']
		url          = request.form['url']
		image_url    = request.form['image-url']
		introduction = request.form['introduction']
		
		new_product_id = Product.add_product(product, url, image_url, introduction)
		return redirect(url_for('single_product', product_id=new_product_id))

# page - edit product
#--------------------------------------------------

# view
@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
	if request.method == 'GET':
		product = Product.get_product(product_id)
		return render_template('edit_product.html', product=product)
	elif request.method == 'POST':
		product      = request.form['product']
		url          = request.form['url']
		image_url    = request.form['image-url']
		introduction = request.form['introduction']

		Product.edit_product(product_id, product, url, image_url, introduction)
		return redirect(url_for('single_product', product_id=product_id))