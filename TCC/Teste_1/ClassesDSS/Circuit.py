# -*- coding: utf-8 -*-


class Circuit(object):

    def __init__(self, dssCircuit):
        self.dssCircuit = dssCircuit

# =============================================================================
#   Circuit
# =============================================================================
    def ActiveCktElement(self):
        return self.dssCircuit.ActiveCktElement

    def ActiveBus(self):
        return self.dssCircuit.ActiveBus

    def Enable(self, Nome_Elemento: str):
        self.dssCircuit.Enable(Nome_Elemento)

    def Disable(self, Nome_Elemento: str):
        self.dssCircuit.Disable(Nome_Elemento)

    def Lines(self):
        return self.dssCircuit.Lines

    def LineCodes(self):
        return self.dssCircuit.LineCodes

    def Loads(self):
        return self.dssCircuit.Loads

    def LoadShapes(self):
        return self.dssCircuit.LoadShapes

    def Transformers(self):
        return self.dssCircuit.Transformers

    def Monitors(self):
        return self.dssCircuit.Monitors

    def Solution(self):
        return self.dssCircuit.Solution

    def Name(self):
        return self.dssCircuit.Name

    def TotalPower(self):
        p = - self.dssCircuit.TotalPower[0]
        q = - self.dssCircuit.TotalPower[1]
        return p, q

    def Buses(self):
        return self.dssCircuit.Buses

    def AllBusDistances(self):
        return self.dssCircuit.AllBusDistances

    def AllBusVmagPu(self):
        return self.dssCircuit.AllBusVmagPu

    def AllNodeDistances(self):
        return self.dssCircuit.AllNodeDistances

    def AllNodeDistancesByPhase(self, Fase: int):
        return self.dssCircuit.AllNodeDistancesByPhase(Fase)

    def AllBusNames(self):
        return self.dssCircuit.AllBusNames

    def AllNodeVmagPUByPhase(self, Fase: int):
        return self.dssCircuit.AllNodeVmagPUByPhase(Fase)

    def SubstationLosses(self):
        return self.dssCircuit.SubstationLosses