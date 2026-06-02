# Fichier main pour démarer le logiciel
# de DALBOURG Théo

from vue import *
from model import *

if __name__ == "__main__":
    # Crée, charge et affiche le logiciel
    vue: VuePrincipale = VuePrincipale()

    # boucle infini de Tk
    vue.run()

    # Sauvegarde et fait d'autre truc avant de couper l'interpréteur Python
    vue.avantFermerProgramme()