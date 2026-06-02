from tkinter import *
from tkinter import messagebox

from model import *

class VueAide(Toplevel):
    """
    Dialogue pour donner les commandes et pour aider
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Aide")

        aideText: Text = Text(self, width=118, height=50)
        aideText.pack()

        AIDE_TEXT:str = """Bienvenue sur la page d'aide pour l'utilisation des pages à Phi-Sciences.

Il y a 200 pages, ce qui est en vert veut dire que l'adhérent à une solde positive, en rouge c'est quand il est négative et en blanc qu'il est à zéro.
Veuillez ne pas nettoyer constamment les pages (en cliquant sur le menu), mais faire une fois par an. Cela supprime tous les pages à solde zéro.

Contrôles:
 * Clique gauche de la sourris: sert à ouvrir la page d'achat, cela permet de passer commande aux adhérent.
 * Clique droit de la sourris: sert à ouvrir l'historique d'achat de la page. Ce qui est en haut c'est les achats les plus récents

Page achat:
 * Il faut juste lire les erreurs parce qu'il exiplique le bon déroulement.
 * Si la page a pas de nom, alors il faut mettre un nom et un prénom
 * OBLIGATOIREMENT mettre un produit qu'il EXISTE dans QUOI?
 * OBLIGATOIREMENT mettre un membre du staff qu'il EXISTE dans QUI?
 * si dans QUOI? c'est un "ajout" ou un "retrait", il faut mettre un valeur POSITIVE
 * puis cliquer sur "validax"

Sauvegarde:
 * A chaque fin de fichier, le fichier est sauvegarder automatiquement.
 * A chaque manipulation d'ajout de membre de staff comme de produit, il sauvegarde
 * A chaque achat le fichier est sauvegardé
 * Vous pouvez faire des Backup avec Sauvegarder As dans l'onglet Fichier. Il va mettre la date du jour sur le fichier
 * A chaque année scolaire, il va créer un nouveau JSON. Il juge que la nouvelle année scolaire est en août pour ceux qui arrive tôt pour tout mettre en ordre.

S'il vous trouvez un bogue, dit à DALBOURG Théo, serveur à Phi-Sciences. S'il n'est pas à l'assosiation, envoyer un courriel à dalbourg2u@etu.univ-lorraine.fr
Dernier modification de la page de vue aide le 6/2/2026
"""

        aideText.insert(END, AIDE_TEXT)

        self.creerButtonBasPage().pack()

    def creerButtonBasPage(self) -> Frame:
        bouttonEnBasFrame = Frame(self)

        validerBoutton = Button(bouttonEnBasFrame, text="Quitter", command=self.destroy)
        validerBoutton.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return bouttonEnBasFrame