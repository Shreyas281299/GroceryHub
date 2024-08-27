from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.productModel import Cart, ProductModel
from app import  db
from utils.cartUtils import updateCart
import razorpay
import os

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/editCart/<kwargs>', methods=['POST'])
@login_required
def edit_cart(kwargs):
    kwargs = eval(kwargs)

    productId = kwargs['productId']
    productToAdd = ProductModel.query.filter_by(productId=productId).first()
    cart = Cart.query.filter_by(userId=current_user.uuid).first()
    productKey = str(productToAdd.productId)
    if 'action' in kwargs.keys():
        action = kwargs['action']
    else:
        action = "add"
    if productKey not in cart.products:
        cart.products[productKey] = 0

    match action:
        case "remove":
            cart.products[productKey] -= 1
            productToAdd.quantityInCart -= 1
            cart.totalValue -= productToAdd.valuePerUnit
        case "add":
            cart.products[productKey] += 1
            productToAdd.quantityInCart += 1
            productToAdd.quantityInStore -= 1
            cart.totalValue += productToAdd.valuePerUnit
        case "clean":
            quantity = cart.products[productKey]
            value = productToAdd.valuePerUnit
            cart.totalValue -= (quantity*value)
            productToAdd.quantityInCart = 0
            cart.products[productKey] = 0
    db.session.commit()
    if 'origin' in kwargs.keys():
        if (kwargs['origin'] == 'cart'):
            return redirect(url_for('cart.cart_view'))
        elif (kwargs['origin'] == 'detailView'):
            return redirect(url_for('product.product_detail_view', productId=kwargs['productId']))
    return redirect(url_for('dashboard.dashboard'))

@cart_bp.route("/cart.html", methods=['POST', 'GET'])
@cart_bp.route('/cart/<message>', methods=['POST', 'GET'])
@login_required
def cart_view(message=None):
    cart = Cart.query.filter_by(userId=current_user.uuid).first()
    total = cart.totalValue
    discount = 0
    if (cart):
        cartData = cart.products
        cartDataProp = {}
        for product in cartData:
            productData = ProductModel.query.filter_by(
                productId=int(product)).first()
            cartDataProp[productData] = cartData[product]
        cartDataProp = {x: y for x, y in cartDataProp.items() if y != 0}
        if current_user.firstOrder:
            discount = 15*total/100
            discountMessage = 'First order discount'
            return render_template('cart.html', cartDataProp=cartDataProp, totalValue=total, message=message, discount=discount, discountMessage=discountMessage)
        return render_template('cart.html', cartDataProp=cartDataProp, totalValue=total, message=message, discount=discount)
    return redirect(url_for('dashboard'))


@cart_bp.route("/handleBuyNow.html", methods=['POST'])
async def handleBuyNow():
    KEY_ID = os.getenv("KEY_ID")
    KEY_SECRET = os.getenv("KEY_SECRET")
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    client.set_app_details({"title" : "flask", "version" : "1.0.0"})
    print(client)
    existingCart = Cart.query.filter_by(userId=current_user.uuid).first()
    changed = updateCart(db, existingCart)
    if changed:
        return redirect(url_for('cart.cart_view', message='Some items in the cart has been updated. Please view the cart.'))
    for product in existingCart.products.keys():
        productToUpdate = ProductModel.query.filter_by(
            productId=int(product)).first()

    order = client.order.create({
        "amount": existingCart.totalValue*100,
        "currency": "INR",
        
    })
    print('_______________________')
    print(order)
    print(client.order.all())
    print('_______________________')

    return render_template('payment.html',order=order,KEY_ID=KEY_ID)

    # Cart.query.filter_by(userId=current_user.uuid).delete()
    # newCart = Cart(userId=current_user.uuid, totalValue=0, products={})
    # current_user.firstOrder = False
    # db.session.add(newCart)
    # db.session.commit()
    # return redirect(url_for('dashboard.dashboard', message="Thank you for your purchase !!"))