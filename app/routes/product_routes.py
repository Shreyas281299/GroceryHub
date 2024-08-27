from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.productModel import ProductModel
from app import db
from app.forms import Product as productForm
from datetime import datetime

product_bp = Blueprint('product', __name__)

@product_bp.route("/addProduct.html", methods=['GET', 'POST'])
def add_product():
    form = productForm.ProductForm()
    if form.validate_on_submit():
        new_product = ProductModel(
            productName=form.productName.data,
            productImage='/static/' + form.productImage.data,
            manufacturingDate=form.manufacturingDate.data,
            expiryDate=form.expiryDate.data,
            quantityInStore=form.quantityInStore.data,
            section=request.form['section'].lower(),
            valuePerUnit=form.valuePerUnit.data,
            addedOnDate=datetime.now()
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('auth.admin', message="Added " + new_product.productName))
    return render_template("addProduct.html", form=form)

@product_bp.route('/productDetailView/<productId>', methods=['POST', 'GET'])
@login_required
def product_detail_view(productId):
    product_data = ProductModel.query.filter_by(productId=productId).first()
    return render_template('productDetailView.html', productData=product_data)


@product_bp.route("/editProduct.html", methods=['POST'])
def edit_product():
    productToEdit = request.form['productToEdit']
    productInStock = request.form['productInStock']
    productEditForm = addProductForm.EditProductForm()
    product = ProductModel.query.filter_by(productName=productToEdit).first()
    try:
        productChangeStock = request.form['changeStock']
    except:
        productChangeStock = False
    if product:
        if productChangeStock == 'changeStock':
            if productInStock == "Out of stock":
                editEngagement(db, product, -5)
                product.quantityInStore = 0
            elif productInStock == "Change stock":
                editEngagement(db, product, +1)
                print("Updating product." + product.productName)
                product.quantityInStore = productEditForm.unitsInStock.data
                product.addedOnDate = datetime.now()
        if productEditForm.productValue.data:
            editEngagement(db, product, +1)
            product.valuePerUnit = productEditForm.productValue.data
        db.session.commit()
        return redirect(url_for('admin', message="Updated "+product.productName))
    else:
        return redirect(url_for('admin', message="Couldn't find the product"))
