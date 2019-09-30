# -*- coding: utf-8 -*-
import numpy as np


class CktElements(object):
    """"""

    def __init__(self, dssCktElement, dssCircuit):
        """Constructor for CktElements"""
        self.dssCktElement = dssCktElement
        self.dssCircuit = dssCircuit

    # =============================================================================
    #   Elements
    # =============================================================================
    def Ativa_Elemento(self, nome_elemento):
        # Ativa elemento pelo seu nome completo "Tipo.Nome"
        if self.dssCircuit.SetActiveElement(nome_elemento) > -1:
            return self.dssCktElement.Name
        else:
            raise Exception('Elemento não existe')

    def get_barras_elemento(self, Nome_Elemento: str = None):
        if Nome_Elemento is not None:
            self.Ativa_Elemento(Nome_Elemento)

        return self.dssCktElement.BusNames

    def Enabled(self, Nome_Elemento: str = None, Ativar: bool = None):
        if Nome_Elemento is not None:
            self.Ativa_Elemento(Nome_Elemento)
        if Ativar is not None:
            self.dssCktElement.Enabled = Ativar

        return self.dssCktElement.Enabled

    def Name(self):
        return self.dssCktElement.Name

    def DisplayName(self):
        return self.dssCktElement.DisplayName

    def NumPhases(self):
        return self.dssCktElement.NumPhases

    def NumConductors(self):
        return self.dssCktElement.NumConductors

    def NumTerminals(self):
        return self.dssCktElement.NumTerminals

    def VoltagesMagAng(self, Nome_Elemento: str = None):
        if Nome_Elemento is not None:
            self.Ativa_Elemento(Nome_Elemento)

        V = self.dssCktElement.VoltagesMagAng
        terminal = self.dssCktElement.NumTerminals

        v1 = []
        ang1 = []
        v2 = []
        ang2 = []

        if terminal == 1:
            for i in range(0, len(V) - 1, 2):
                v1.append(V[i])
                ang1.append(V[i + 1])
        else:
            for i in range(0, len(V) - 1, 2):
                if i < len(V) / 2:
                    v1.append(V[i])
                    ang1.append(V[i + 1])
                else:
                    v2.append(V[i])
                    ang2.append(V[i + 1])

        return v1, v2, ang1, ang2

    def Voltages(self):
        return self.dssCktElement.Voltages

    def Powers(self, Nome_Elemento: str = None):
        if Nome_Elemento is not None:
            self.Ativa_Elemento(Nome_Elemento)

        S = self.dssCktElement.Powers
        terminal = self.dssCktElement.NumTerminals

        p1 = []
        p2 = []
        if terminal == 1:
            for i in range(0, len(S) - 1, 2):
                p1.append(np.complex(S[i], S[i + 1]))
        else:
            for i in range(0, len(S) - 1, 2):
                if i < len(S) / 2:
                    p1.append(np.complex(S[i], S[i + 1]))
                else:
                    p2.append(np.complex(S[i], S[i + 1]))

        return p1, p2

    def TotalPower(self, Nome_Elemento: str = None):
        if Nome_Elemento is not None:
            self.Ativa_Elemento(Nome_Elemento)

        p1, p2 = self.Powers()

        p1_total = np.sum(p1)
        p2_total = np.sum(p2)

        return p1_total, p2_total

    def PhaseLosses(self):
        return self.dssCktElement.PhaseLosses