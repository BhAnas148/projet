## table user
- id
- nom
- prenom
- date de naissance
- telephone
- ville
- adresse
- email
- mot_de_passe
- role (client, fournisseur, analyste, gestionnaire, commercial, administrateur)

## table categorie
- id
- nom

## table sous-categorie
- id
- categorie_id
- nom

## table produit
- id
- categorie_id
- sous_categorie_id
- designation
- description
- prix_vente

## table image
- id
- produit_id
- nom
- is_primary

## table commande
- id
- client_id (table user)
- montant_total
- nb_article
- date_creation

## table commande_produit
- id
- commande_id
- produit_id
- prix_unitaire
- quantite
- prix_total

## table achat
- id
- produit_id
- fournisseur_id
- prix_achat_unitaire
- quantite
- prix_achat_total
- date_creation