from collections import Counter
from sqlalchemy import text

from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request

from src import db

from src.controllers.UserController import UserController
from src.controllers.CategorieController import CategorieController
from src.controllers.SousCategorieController import SousCategorieController
from src.controllers.ProduitController import ProduitController
from src.controllers.ImageController import ImageController

from src.routes.utils import is_logged_in


frontend_routes = Blueprint('frontend', __name__)


def generate_cart_suggestions():
    cart = session.get('cart', [])
    if not cart:
        session['cart_suggestions'] = []
        return []

    cart_product_ids = [int(item) for item in cart.keys()]

    # Raw SQL for performance (optional: convert to SQLAlchemy ORM query)
    query = text("""
        SELECT cp2.produit_id
        FROM commande_produit cp
        JOIN commande_produit cp2 ON cp.commande_id = cp2.commande_id
        WHERE cp.produit_id = ANY(:cart_ids) AND cp2.produit_id != ALL(:cart_ids)
    """)

    result = db.session.execute(query, {"cart_ids": cart_product_ids})
    suggested_ids = [row[0] for row in result.fetchall()]

    # Count frequency of each suggested product ID
    counts = Counter(suggested_ids)
    top_suggestions = [prod_id for prod_id, _ in counts.most_common(3)]

    if not top_suggestions:
        session['cart_suggestions'] = []
        return []

    # Fetch product info (designation, prix_vente, image, etc.)
    products = db.session.execute(text("""
        SELECT p.id, p.designation, p.prix_vente,
               (SELECT nom FROM image WHERE produit_id = p.id AND is_primary = true LIMIT 1) as image
        FROM produit p
        WHERE p.id = ANY(:ids)
    """), {"ids": top_suggestions}).fetchall()

    # Convert to dict format
    suggestions = [{
        "produit_id": row[0],
        "designation": row[1],
        "prix_vente": float(row[2]),
        "image": row[3]
    } for row in products]

    # session['cart_suggestions'] = suggestions
    return suggestions


@frontend_routes.route('/<sous_categorie_id>/produits')
def produits(sous_categorie_id):
    sous_categorie = SousCategorieController.read_one(sous_categorie_id)
    if not sous_categorie:
        produits = ProduitController.read_all()
    else:
        produits = ProduitController.read_by_sous_categorie(sous_categorie_id)

    categories = CategorieController.read_all()
    sous_categories = SousCategorieController.read_all()

    return render_template(
        'frontend/produits/index.html',
        produits=produits,
        sous_categorie=sous_categorie,
        type='sous_categorie',
        categories=categories,
        sous_categories=sous_categories
    )


@frontend_routes.route('/<sous_categorie_id>/produits/<produit_id>')
def produit_detail(sous_categorie_id, produit_id):
    produit = ProduitController.read_one(produit_id)
    if not produit:
        flash('Produit non trouvé.', 'danger')
        return redirect(url_for('frontend.produits', sous_categorie_id=sous_categorie_id))

    return render_template(
        'frontend/produits/detail.html',
        produit=produit
    )


@frontend_routes.route('/cart')
def cart():
    suggestions = generate_cart_suggestions()
    return render_template('frontend/cart/index.html', suggestions=suggestions)


@frontend_routes.route('/add_to_cart/<suggestion_produit_id>')
def add_to_cart_with_suggestion(suggestion_produit_id):
    produit = ProduitController.read_one(suggestion_produit_id)
    if not produit:
        flash('Produit non trouvé.', 'danger')
        return redirect(url_for('frontend.cart'))

    image = ImageController.read_primary(suggestion_produit_id)

    # Get cart from session or create new one
    cart = session.get('cart', {})

    # If product already in cart, update quantity
    if suggestion_produit_id in cart:
        cart[suggestion_produit_id]['quantity'] += 1
    else:
        cart[suggestion_produit_id] = {
            'designation': produit.designation,
            'image': image.nom if image else None,
            'prix_vente': produit.prix_vente,
            'quantity': 1
        }

    # Save cart back to session
    session['cart'] = cart

    # Recalculate total
    total = sum(
        item['prix_vente'] * item['quantity'] for item in cart.values()
    )
    session['total'] = round(total, 2)  # optional rounding

    return redirect(url_for('frontend.cart'))


@frontend_routes.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    produit_id = str(data.get('produit_id'))  # keys must be str for session
    designation = data.get('designation')
    image = data.get('image')
    prix_vente = float(data.get('prix_vente'))
    quantity = int(data.get('quantity'))

    if not all([produit_id, designation, image, prix_vente, quantity]):
        return jsonify({'message': 'Invalid data.'}), 400

    # Get cart from session or create new one
    cart = session.get('cart', {})

    # If product already in cart, update quantity
    if produit_id in cart:
        cart[produit_id]['quantity'] += quantity
    else:
        cart[produit_id] = {
            'designation': designation,
            'image': image,
            'prix_vente': prix_vente,
            'quantity': quantity
        }

    # Save cart back to session
    session['cart'] = cart

    # Recalculate total
    total = sum(
        item['prix_vente'] * item['quantity'] for item in cart.values()
    )
    session['total'] = round(total, 2)  # optional rounding

    return jsonify({'message': 'Produit ajouté au panier.', 'total': session['total']}), 200


@frontend_routes.route('/remove_from_cart/<produit_id>')
def remove_from_cart(produit_id):
    produit_id = str(produit_id)
    cart = session.get('cart', {})
    if produit_id in cart:
        del cart[produit_id]
        session['cart'] = cart

        # Recalculate total
        total = sum(
            item['prix_vente'] * item['quantity'] for item in cart.values()
        )
        session['total'] = round(total, 2)

    return redirect(url_for('frontend.cart'))


@frontend_routes.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    updated_cart = data.get('cart', {})
    shipping = float(data.get('shipping', 0))

    cart = session.get('cart', {})
    # Update quantities in session cart
    for key, qty in updated_cart.items():
        if key in cart:
            cart[key]['quantity'] = int(qty)
    session['cart'] = cart

    # Update shipping in session or however you track it
    session['shipping'] = shipping

    # Optionally recalc total
    total = sum(item['quantity'] * item['prix_vente']
                for item in cart.values())
    session['total'] = total

    return jsonify({'success': True})


@frontend_routes.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.pop('total', None)
    session.pop('shipping', None)
    return jsonify({'success': True})


@frontend_routes.route('/wishlist')
@is_logged_in
def wishlist():
    return render_template('frontend/wishlist.html')


@frontend_routes.route('/contact')
def contact():
    return render_template('frontend/contact.html')


@frontend_routes.route('/tos')
def tos():
    return render_template('frontend/tos.html')


@frontend_routes.route('/privacy')
def privacy():
    return render_template('frontend/privacy.html')


@frontend_routes.route('/about')
def about():
    return render_template('frontend/about.html')


@frontend_routes.route('/mes-commandes')
def mes_commandes():
    return render_template('frontend/commandes/index.html')


@frontend_routes.route('/profile')
@is_logged_in
def profile():
    user_id = session.get('user_id')
    user = UserController.read_one(user_id)

    if session.get('user_role') == 'client':
        return render_template('frontend/profile.html', user=user)

    return render_template('profile.html', user=user)


@frontend_routes.route('/profile/edit', methods=['POST'])
@is_logged_in
def profile_edit():
    flash('This feature is not yet implemented.', 'warning')
    return redirect(url_for('frontend.profile'))


@frontend_routes.route('/profile/edit/password', methods=['POST'])
@is_logged_in
def profile_edit_password():
    flash('This feature is not yet implemented.', 'warning')
    return redirect(url_for('frontend.profile'))
