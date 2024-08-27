from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.models.productModel import ProductModel
from app import db
from utils.cartUtils import cart_init

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['POST', 'GET'])
@dashboard_bp.route('/dashboard/<message>', methods=['POST', 'GET'])
@login_required
def dashboard(message=None):
    cart_init(db, current_user)
    print('Loading dashboard')
    productDataArray = ProductModel.query.all()
    freshProducts = ProductModel.query.order_by(
        desc(ProductModel.addedOnDate))[:6]
    return render_template('dashboard.html', UserModel=current_user, productDataArray=productDataArray, message=message, freshProducts=freshProducts)
