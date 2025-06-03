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
@home_routes.route('/les_produit')
#@is_logged_in
def les_produit():
    return render_template('frontend/les_produit.html')
@home_routes.route('/contact')
#@is_logged_in
def contact():
    return render_template('frontend/contact.html')
@home_routes.route('/vérifier')
#@is_logged_in
def vérifier():
    return render_template('frontend/vérifier.html')
@home_routes.route('/produit_details')
#@is_logged_in
def produit_details():
    return render_template('frontend/produit_details.html')
@home_routes.route('/compte')
#@is_logged_in
def compte():
    return render_template('frontend/compte.html')