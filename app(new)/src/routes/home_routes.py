from flask import Blueprint, render_template, session

from src.routes.utils import is_logged_in

home_routes = Blueprint('home', __name__)


@home_routes.route('/')
#@is_logged_in
def home():
    if 'LOGGED_IN' in session and session.get('user_role', '') in ['fournisseur', 'analyste', 'commercial', 'administrateur']:
        return render_template('index.html')
    
    return render_template('frontend/index.html')
    
@home_routes.route('/cart')
#@is_logged_in
def cart():
    return render_template('frontend/cart.html')

@home_routes.route('/about')
#@is_logged_in
def about():
    return render_template('frontend/about.html')
@home_routes.route('/el_produit')
#@is_logged_in
def el_produit():
    return render_template('frontend/el_produit.html')