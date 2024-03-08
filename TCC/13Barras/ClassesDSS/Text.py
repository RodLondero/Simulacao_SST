# -*- coding: utf-8 -*-

class Text(object):
    """"""

    def __init__(self, dssText):
        """Constructor for Text"""
        self.dssText = dssText

    def Command(self, Comando: str):
        self.dssText.Command = Comando
        return self.dssText.Result
