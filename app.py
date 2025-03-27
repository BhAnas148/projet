from flask import Flask, render_template

from blueprints.categories import categories_blueprint
from blueprints.sous_categories import sous_categories_blueprint
from blueprints.clients import clients_blueprint
from blueprints.commandes import commandes_blueprint
from blueprints.produits import produits_blueprint
from blueprints.fournisseurs import fournisseurs_blueprint

app = Flask(__name__)
app.secret_key = "c1430b67605ee5c9f36b999d332c5f2305cf210d"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5432/pfe"

app.register_blueprint(categories_blueprint, url_prefix='/categories')
app.register_blueprint(sous_categories_blueprint,
                       url_prefix='/sous-categories')
app.register_blueprint(clients_blueprint, url_prefix='/clients')
app.register_blueprint(commandes_blueprint, url_prefix='/commandes')
app.register_blueprint(produits_blueprint, url_prefix='/produits')
app.register_blueprint(fournisseurs_blueprint, url_prefix='/fournisseurs')


@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/login")
# def login():
#     return render_template('login.html')

# @app.route('/clients')
# def clients_index():
#     return render_template('clients/index.html')

# @app.route('/commandes')
# def commandes_index():
#     return render_template('commandes/index.html')

# @app.route('/produits')
# def produits_index():
#     return render_template('produits/index.html')
# @app.route('/fournisseurs')
# def fournisseurs_index():
#     return render_template('fournisseurs/index.html')


if __name__ == '__main__':
    app.run(debug=True)
