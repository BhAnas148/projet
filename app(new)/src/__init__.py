from flask import Flask

from src.entities import db

from src.routes.categorie_routes import categorie_routes
from src.routes.sous_categorie_routes import sous_categorie_routes
from src.routes.produit_routes import produit_routes
from src.routes.commande_routes import commande_routes
from src.routes.commande_produit_routes import commande_produit_routes
from src.routes.achat_routes import achat_routes
from src.routes.fournisseur_routes import fournisseur_routes
from src.routes.client_routes import client_routes
from src.routes.commercial_routes import commercial_routes
from src.routes.analyste_routes import analyste_routes 
from src.routes.image_routes import image_routes

from src.routes.user_routes import user_routes
from src.routes.home_routes import home_routes

from src.routes.seeder_routes import seeder_routes


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('config.Config')
    db.init_app(app)

    # Blueprints
    app.register_blueprint(categorie_routes)
    app.register_blueprint(sous_categorie_routes)
    app.register_blueprint(produit_routes)
    app.register_blueprint(commande_routes)
    app.register_blueprint(commande_produit_routes)
    app.register_blueprint(achat_routes)
    app.register_blueprint(fournisseur_routes)
    app.register_blueprint(client_routes)
    app.register_blueprint(commercial_routes)
    app.register_blueprint(analyste_routes) 
    app.register_blueprint(image_routes) 

    app.register_blueprint(user_routes, url_prefix='/')
    app.register_blueprint(home_routes, url_prefix='/')

    app.register_blueprint(seeder_routes, url_prefix='/seeder')

    return app
