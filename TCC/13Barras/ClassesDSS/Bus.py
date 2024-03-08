# -*- coding: utf-8 -*-


class Bus(object):

    def __init__(self, dssCircuit, dssBus):
        self.dssCircuit = dssCircuit
        self.dssBus = dssBus

    # ------------------------------------------------------------------------------------------------------------------
    def set_barra_by_name(self, Nome_Barra: str):
        self.dssCircuit.SetActiveBus(Nome_Barra)
        return self.dssBus.Name
    # ------------------------------------------------------------------------------------------------------------------
    def Distance(self):
        return self.dssBus.Distance
    # ------------------------------------------------------------------------------------------------------------------
    def kVBase(self, Barra: str = None):
        if Barra is not None:
            self.dssCircuit.SetActiveBus(Barra)

        return self.dssBus.kVBase
    # ------------------------------------------------------------------------------------------------------------------
    def VMagAngle(self):
        return self.dssBus.VMagAngle
    # ------------------------------------------------------------------------------------------------------------------
    def puVoltages(self):
        return self.dssBus.puVoltages
    # ------------------------------------------------------------------------------------------------------------------
    def puVmagAngle(self):
        return self.dssBus.puVmagAngle
    # ------------------------------------------------------------------------------------------------------------------