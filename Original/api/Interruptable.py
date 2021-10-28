# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 00:23:48 2020

@author: hutton
"""

class Interruptable:
    """Classe intégrant une boucle sans fin pouvant être stoppée proprement."""

    interruptables = []

    def __init__(self):
        """Crée un objet interruptible."""

        self._interrupted = False
        Interruptable.interruptables.append(self)

    def interrupt(self):
        """Envoi la demande d'arrêt."""

        self._interrupted = True

    def reset(self):
        """Permet le redémarrage d'un service."""

        self._interrupted = False

    def interrupted(self):
        """Verifie si la demande d'arrêt à déjà été envoyée."""

        return self._interrupted
