from tkinter import messagebox

class MessageErreurs:
    @staticmethod
    def get_format_ligne(ligne: int|str, message: str) -> str:
        """
        Donne le format sur la gestion de l'affichage d'erreur. Si vous ne précisez pas où il se situe, alors il n'affice que le message
        """
        return message if ligne == "" else f"Erreur sur la ligne: {ligne}\n{message}"

    @staticmethod
    def encodement(ligne: int|str=""):
        messagebox.showerror(
                title="Erreur d'encodement de la valeur", 
                message=MessageErreurs.get_format_ligne(ligne, "Vous devez écrire un chiffre sous la forme 18,55 ou 0,34. De plus ce chiffre doit être positif")
            )
    
    @staticmethod
    def formatage(explication:str, ligne: int|str=""):
        messagebox.showerror(
                title="Erreur de formatage de la valeur", 
                message=MessageErreurs.get_format_ligne(ligne, explication)
            )

    @staticmethod
    def valeur_negative(ligne: int|str=""):
        messagebox.showerror(
                title="Valeur négative", 
                message=MessageErreurs.get_format_ligne(ligne, "La valeur doit être toujours positif")
            )
    
    @staticmethod
    def manque_valeur(valeur_manquante: str, champs:str = "", ligne: int|str=""):
        messagebox.showerror(
                title=f"Vous devez mettre la valeur {valeur_manquante}", 
                message=MessageErreurs.get_format_ligne(ligne, f"Vous devez mettre une valeur dans {valeur_manquante if champs == "" else champs}")
            )
    
    @staticmethod
    def valeur_indesponible(valeur: str, ligne: int|str=""):
        messagebox.showerror(
            title=f"la valeur {valeur} est indisponible",
            message=MessageErreurs.get_format_ligne(ligne, f"La valeur << {valeur} >> n'est pas disponible dans le logiciel")
        )