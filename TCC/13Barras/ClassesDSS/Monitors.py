# -*- coding: utf-8 -*-


class Monitors(object):
    """"""

    def __init__(self, dssMonitors):
        """Constructor for Monitors"""
        self.dssMonitors = dssMonitors

    def getDados(self, Nome_Monitor: str, Canais: int or list, base: float = None):
        self.Name(Nome_Monitor)
        dados = []
        if type(Canais) == list:
            for i in Canais:
                valor = self.Channel(i)
                if base is not None:
                    valor = [x/base for x in valor]
                dados.append(valor)
        else:
            dados = self.Channel(Canais)
            if base is not None:
                dados = [x / base for x in dados]
        return dados

    def Name(self, Nome_Monitor: str = None):
        if Nome_Monitor is not None:
            self.dssMonitors.Name = Nome_Monitor
        return self.dssMonitors.Name

    def AllNames(self):
        return self.dssMonitors.AllNames

    def ByteStream(self):
        return self.dssMonitors.ByteStream

    def Element(self):
        return self.dssMonitors.Element

    def Terminal(self):
        return self.dssMonitors.Terminal

    def Mode(self):
        return self.dssMonitors.Mode

    def Channel(self, Canal: int):
        return self.dssMonitors.Channel(Canal)

    def Save(self):
        self.dssMonitors.Save()

    def SaveAll(self):
        self.dssMonitors.SaveAll()

    def Show(self):
        self.dssMonitors.Show()

    def SampleCount(self):
        return self.dssMonitors.SampleCount

    def Reset(self):
        return self.dssMonitors.Reset()