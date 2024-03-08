# -*- coding: utf-8 -*-


class Loads(object):
    """Classe para manipular as Loads"""

    def __init__(self, dssLoads):
        self.dssLoads = dssLoads

    def Name(self, Nome_Carga: str = None):
        if Nome_Carga is None:
            return self.dssLoads.Name
        else:
            self.dssLoads.Name = Nome_Carga
            return self.dssLoads.Name

    def kV(self, kV: float = None):
        """
        Se kv is none - Retorna o valor de kV da carga\n
        Se kv possuir valor - atribuir esse valor ao kV da carga
        """
        if kV is None:
            return self.dssLoads.kV
        else:
            self.dssLoads.kV = kV
            return self.dssLoads.kV

    def kW(self, kW: float = None):
        if kW is None:
            return self.dssLoads.kW
        else:
            self.dssLoads.kW = kW
            return self.dssLoads.kW

    def kvar(self, kvar: float = None):
        if kvar is None:
            return self.dssLoads.kvar
        else:
            self.dssLoads.kvar = kvar
            return self.dssLoads.kvar

    def kva(self, kva: float = None):
        if kva is None:
            return self.dssLoads.kva
        else:
            self.dssLoads.kva = kva
            return self.dssLoads.kva

    def PF(self, fp: float = None):
        if fp is None:
            return self.dssLoads.PF
        else:
            self.dssLoads.PF = fp
            return self.dssLoads.PF

    def daily(self, LoadShape: str = None):
        if LoadShape is None:
            return self.dssLoads.daily
        else:
            self.dssLoads.daily = LoadShape
            return self.dssLoads.daily

    def First(self):
        return self.dssLoads.First

    def Next(self):
        return self.dssLoads.Next

    def Count(self):
        return self.dssLoads.Count

    def IsDelta(self):
        return self.dssLoads.IsDelta

    def Model(self):
        return self.dssLoads.Model

    def vminpu(self, vminpu = None):
        if vminpu is None:
            return self.dssLoads.Vminpu
        else:
            self.dssLoads.Vminpu = vminpu
            return self.dssLoads.Vminpu

    def vmaxpu(self, vmaxpu = None):
        if vmaxpu is None:
            return self.dssLoads.Vmaxpu
        else:
            self.dssLoads.Vmaxpu = vmaxpu
            return self.dssLoads.Vmaxpu