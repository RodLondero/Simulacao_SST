# -*- coding: utf-8 -*-


class Transformers(object):

    def __init__(self, dssTransformers):
        self.dssTransformers = dssTransformers

    def Name(self, Nome_Transformador: str = None):
        if Nome_Transformador is None:
            return self.dssTransformers.Name
        else:
            self.dssTransformers.Name = Nome_Transformador
            return self.dssTransformers.Name

    def kV(self, terminal: int, kV: float = None):
        # Ativar um dos terminais do transformador
        self.dssTransformers.Wdg = terminal
        if kV is None:
            return self.dssTransformers.kV
        else:
            self.dssTransformers.kV = kV
            return self.dssTransformers.kV

    def kva(self, terminal: int, kva: float = None):
        self.dssTransformers.Wdg = terminal
        if kva is None:
            return self.dssTransformers.kva
        else:
            self.dssTransformers.kva = kva
            return self.dssTransformers.kva

    def getTaps(self, terminal: int):
        self.Wdg(terminal)
        taps = {'MinTap': self.dssTransformers.MinTap,
                'MaxTap': self.dssTransformers.MaxTap,
                'NumTaps': self.dssTransformers.NumTaps}

        return taps

    def Tap(self, terminal: int, Tap: float = None):
        self.dssTransformers.Wdg = terminal
        if Tap is None:
            return self.dssTransformers.Tap
        else:
            self.dssTransformers.Tap = Tap
            return self.dssTransformers.Tap

    def Wdg(self, terminal: int = None):
        if terminal is None:
            return self.dssTransformers.Wdg
        else:
            self.dssTransformers.Wdg = terminal
            return self.dssTransformers.Wdg

    def First(self):
        return self.dssTransformers.First

    def Next(self):
        return self.dssTransformers.Next

    def Count(self):
        return self.dssTransformers.Count