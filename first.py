from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017/")
db=client["ecommerceDB"]
produits_col=db["produits"]                        
clients_col=db["clients"]                        
commandes_col=db["commandes"]   

from datetime import datetime
#1
def creer_commande():
    client_nom=input("entrez le nom du client:")
    client_doc=clients_col.find_one({"Nom":client_nom})
    if not client_doc:
        print("client introuvable.")
        return
    details_produits=[]
    total = 0

    while True:
        nom_produit = input("nom du produit a ajouter (ou 'fin' pour terminer):")
        if nom_produit.lower()=="fin":
            break
        quantite=int(input(f"quantite de '{nom_produit}':"))
        produit=produits_col.find_one({"Nom": nom_produit})
        if produit and produit["Stock"]>=quantite:
            total+=produit["Prix"]*quantite
            details_produits.append({"produit":nom_produit, "quantite":quantite})
            produits_col.update_one({"Nom":nom_produit}, {"$inc":{"Stock":-quantite}})
        else:
            print(f"Produit '{nom_produit}' introuvable ou stock insuffisant.")
    if details_produits:
        commande = {"Client": client_nom,"Produits": details_produits, "Date_commande": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Statut": "en cours","Montant_total": total}
        commandes_col.insert_one(commande)
        print("Commande cree avec succee.")
    else:
        print("aucun produit ajoute.")

#2
def afficher_produits():
    produits=produits_col.find()
    for p in produits:
        print(f"Nom: {p['Nom']}, Prix: {p['Prix']}, Stock: {p['Stock']}, Catégorie: {p['Catégorie']}")

afficher_produits()

def rechercher_commandes_client():
    nom=input("entrez le nom du client:")
    commandes=commandes_col.find({"Client":nom})
    for c in commandes:
        print(c)

# 4
def rechercher_commandes_livrees():
    commandes=commandes_col.find({"Statut":"livrée"})
    for c in commandes:
        print(c)

# 5
def update_produit():
    nom=input("nom du produit a modifier:")
    nouveau_prix=float(input("nouveau prix:"))
    produits_col.update_one({"Nom": nom}, {"$set":{"Prix": nouveau_prix}})
    print("produit mis a jour avec succes.")



# 6
def ajouter_dispo():
    produits_col.update_many({},{"$set":{"disponible":True}})
    print("champ disponible ajoute a tous les produits.")


# 7
def supprimer_commande_produit_client():
    nom=input("entrez nom du client:")
    produit=input("nom du produit dans la commande:")
    commandes_col.delete_many({"Client": nom, "Produits": {"$regex": produit, "$options": "i"}})
    print("commande supprimee si elle existait.")

# 8
def supprimer_commandes_client():
    nom=input("entrez nom du client:")
    commandes_col.delete_many({"Client":nom})
    print(f"toutes les commandes du client {nom} a ete supprimee.")


# 9
def trier_commandes_par_date():
    commandes=commandes_col.find().sort("Date_commande",-1)
    for c in commandes:
        print(c)

# 10
def afficher_produits_dispo():
    produits=produits_col.find({"Stock":{"$gt":0}})
    for p in produits:
        print(p)

def afficher_tous_produits():
    produits=produits_col.find()
    for p in produits:
        print(p)

# 11
def menu():
    while True:
        print("\n===== MENU =====")
        print("1. Ajouter une commande")
        print("2. Afficher tous les produits")
        print("3. Afficher les produits disponibles")
        print("4. Rechercher un commandes par client")
        print("5. Mettre à jour un produit")
        print("6. Supprimer une commande")
        print("7. Supprimer les commandes d’un client donné ")
        print("8. Afficher les produits disponibles ")
        print("9. Trier les commandes par date de la commande")
        print("10. Quitter")
        choix = input("entrez votre choix:")

        if choix=="1":
            creer_commande()
        elif choix=="2":
            afficher_tous_produits()
        elif choix=="3":
            afficher_produits_dispo()
        elif choix=="4":
            rechercher_commandes_client()
        elif choix=="5":
            update_produit()
        elif choix=="6":
            supprimer_commande_produit_client()
        elif choix=="7":
            supprimer_commandes_client()
        elif choix=="8":
            ajouter_dispo()
        elif choix=="9":
            trier_commandes_par_date()
        elif choix=="10":
            print("au revoir.")
            break
        else:
            print("choix invalide.")


menu()

