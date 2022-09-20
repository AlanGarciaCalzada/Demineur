"""
Fichier contenant la classe "Case".
"""

class Case:
    """
    Permet de faire une case qui peut contenir une bombe,
    a la capacité d'être activé (une fois activée, elle ne peut pas être désactivé),
    note le nombre de bombes qu'il y a autour d'elle (cela se fait manuellement),
    elle peut posséder un drapeau et dans ce cas elle ne peut pas être activé.
    """

    def __init__(self, bomb):
        self.has_bomb = bomb
        self.is_activated = False
        self.is_flagged = False
        self.bombs_around = 0
        self.bombs_around_test = 0

    def activate(self):
        """
        Permet d'activer le case.
        """
        if not self.is_flagged:
            self.is_activated = True
        return self.is_activated

    def add_bomb_around(self):
        """
        Permet d'incrémenter la valeur permettant de savoir combien de bombes
        il y a autour de la case.
        """
        self.bombs_around += 1
        self.bombs_around_test += 1

    def switch_flag(self):
        """
        Permet de mettre un drapeau sur la case (l'empêche d'être activé).
        """
        if not self.is_activated:
            self.is_flagged = not self.is_flagged
