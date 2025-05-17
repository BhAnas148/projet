import sys
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

# Add your application directory to the path
sys.path.append('./main.py')

from main import db, create_app
from src.entities.user import User, UserRole
from src.entities.commande_produit import CommandeProduit
from src.entities.commande import Commande
from src.entities.produit import Produit
from src.entities.categorie import Categorie
from src.entities.sous_categorie import SousCategorie
from src.entities.image import Image
from src.entities.achat import Achat

def clear_database():
    """Delete all records in proper order to respect foreign key constraints"""
    try:
        
        db.session.query(CommandeProduit).delete()
        db.session.query(Commande).delete()
        db.session.query(Achat).delete()
        
        db.session.query(Image).delete()
        
        db.session.query(Produit).delete()
       
        db.session.query(SousCategorie).delete()
        db.session.query(Categorie).delete()
        
        num_users = db.session.query(User).delete()
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing database: {str(e)}")
        return False

def create_default_users():
    app = create_app()
    with app.app_context():
        try:
            # Clear the entire database first
            if not clear_database():
                return
            
            # Default users data
            default_users = [
                {
                    "nom": "Client",
                    "prenom": "Demo",
                    "email": "client@gmail.com",
                    "mot_de_passe": "123456",
                    "role": UserRole.client,
                    "telephone": "0612345678",
                    "ville": "Casablanca",
                    "adresse": "123 Rue Client",
                    "date_de_naissance": datetime(1990, 1, 1)
                },
                {
                    "nom": "Fournisseur",
                    "prenom": "Demo",
                    "email": "fournisseur@gmail.com",
                    "mot_de_passe": "123456",
                    "role": UserRole.fournisseur,
                    "telephone": "0622345678",
                    "ville": "Rabat",
                    "adresse": "456 Rue Fournisseur",
                    "date_de_naissance": datetime(1985, 5, 15)
                },
                {
                    "nom": "Analyste",
                    "prenom": "Demo",
                    "email": "analyste@gmail.com",
                    "mot_de_passe": "123456",
                    "role": UserRole.analyste,
                    "telephone": "0632345678",
                    "ville": "Marrakech",
                    "adresse": "789 Rue Analyste",
                    "date_de_naissance": datetime(1988, 8, 20)
                },
                {
                    "nom": "Commercial",
                    "prenom": "Demo",
                    "email": "commercial@gmail.com",
                    "mot_de_passe": "123456",
                    "role": UserRole.commercial,
                    "telephone": "0652345678",
                    "ville": "Fès",
                    "adresse": "202 Rue Commercial",
                    "date_de_naissance": datetime(1992, 7, 25)
                },
                {
                    "nom": "Admin",
                    "prenom": "System",
                    "email": "admin@gmail.com",
                    "mot_de_passe": "123456",
                    "role": UserRole.administrateur,
                    "telephone": "0662345678",
                    "ville": "Agadir",
                    "adresse": "303 Rue Admin",
                    "date_de_naissance": datetime(1980, 12, 5)
                }
            ]

            # Create and add users
            users_created = 0
            for user_data in default_users:
                user = User(
                    nom=user_data["nom"],
                    prenom=user_data["prenom"],
                    email=user_data["email"],
                    mot_de_passe=sha256.hash(user_data['mot_de_passe']),
                    role=user_data["role"],
                    telephone=user_data["telephone"],
                    ville=user_data["ville"],
                    adresse=user_data["adresse"],
                    date_de_naissance=user_data["date_de_naissance"]
                )
                db.session.add(user)
                users_created += 1

            db.session.commit()
            print(f"Successfully created {users_created} default users.")
            
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")
            raise

if __name__ == '__main__':
    create_default_users()