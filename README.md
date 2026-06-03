# Pages de Phi-Sciences

Le but est de faire une mini interface graphique pour gérer les pages dans l'association étudiante à Phi-Sciences. Il contient 200 pages, et il doit gérer l'ajout, la supprésion des pages vide, et les produits comme faire des backup.

# Pourquoi j'ai fait ça

Avant le système, nous utilisions excel, ça marchait superbien mais il fallait se reconnecter constament. Il a fallu trouvé une alternative libre, sans payer, et facile à maintenir pour les générations futurs.

# Ceux qui me lit

Vous devez être sûrement en licence d'informatique, et là vous êtes dans une situation difficile car le code ne marche plus. Je vous invite d'écrire du code en français, même les nom de fonction, suivez une cohérence du code.

# Comment ça marche ?

Il y a 3 modules:

* le modèle, c'est le cerveau du projet, il trie les produits, il gère les adhérents, il gère les achats.
* les services, ça sert essentielement à demander de faire des choses sur le modèle comme sauvegarder comme charger (c'est de la sérialisation), comme mettre une base de donnée avec sqlLite (la persistence), ou bien des appels d'API
* les vues, ça sert à faire l'affichage général de notre modèle. Une vue intéragie sur le modèle.

# Dépendance

Vous devez concraitement connaître Tkinter car c'est dans la librairie natif de python3, et votre cours d'interface graphiaque (bonne chance pour le projet de synthèse >_<)

# Mot de la fin

Merci d'avoir lu, et tous ceux qui ajoute ou corrige un bug, veuillé augmenté de 1 le nombre de la version, et ajouter votre nom sur la liste des développeurs avec un petit commentaire s'il vous voulez. Bisou

# Les versions

* v1.0 - **Créations et sauvetage des pages** - de *DALBOURG Théo*.
  * Gestion du modèle
  * Gestion des sauvegarde en JSON avec la sérialisation
  * Gestion des vue avec TKinter
    * une page principal avec tous les adhérents
    * une page (de dialog) pour faire payer nos produits
    * une page (de dialog) pour modifier nos produits
    * une page (de dialog) pour modifier le staff et le président
  * Gestion d'ouverture automatique du fichier JSON de l'année en cours
  * Création automatique du fichier JSON de l'année en cours. Change en août
  * Beaucoup de protections sur les achats (vérification sur la solde avant de payer !!!!)
  * Historique des achats en général sur le modèle comme sur les adhérents comme pouvoir les lire
  * Catégorie des produtis avec leur petit stats
  * Un petit onglet aide
  * gestion automatique de création de fichier à chaque année scolaire (et nettoie les pages)