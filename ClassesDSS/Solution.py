# -*- coding: utf-8 -*-

from ClassesDSS.Options import ControlModes, SolveModes
import time

class Solution(object):
    """"""

    def __init__(self, dssSolution, dssText):
        """Constructor for Solution"""
        self.dssSolution = dssSolution
        self.dssText = dssText

    def Converged(self):
        return self.dssSolution.Converged

    def SnapShot(self, multiplicador_carga: float = None, ControlMode: int = None):
        # Configurações
        self.dssSolution.Mode = SolveModes.dssSnapShot
        self.dssSolution.ControlMode = ControlModes.dssControlOFF if ControlMode is None else ControlMode

        # Multiplicar o valor nominal das cargas pelo valor do
        # multiplicador_carga
        if multiplicador_carga is not None:
            self.dssSolution.LoadMult = multiplicador_carga

        self.dssText.Command("Set Voltagebases=[115, 13.8, '@VL']")
        self.dssText.Command("calcvoltagebases")
        # Resolver o Fluxo de Potência
        self.dssSolution.Solve()
        time.sleep(0.1)

    def Daily(self, passo: str, time_inicial: tuple, numero, ControlMode: int = None):

        self.ModeDaily()
        self.dssSolution.ControlMode = ControlModes.dssControlOFF if ControlMode is None else ControlMode
        self.Number(numero)
        self.dssSolution.MaxIterations = 100
        self.dssSolution.MaxControlIterations = 100
        self.Hour(time_inicial[0])

        self.dssText.Command("Set stepsize={passo} time={time_inicial}".format(passo=passo,
                                                                               time_inicial=time_inicial))
        # if hora_minuto_segundo == 'h':
        #     self.StepsizeHr(passo)
        # elif hora_minuto_segundo == 'm':
        #     self.StepsizeMin(passo)
        # elif hora_minuto_segundo == 's':
        #     self.StepSize(passo)

        self.dssSolution.Solve()
        # print("Solve: " + "Sucesso" if self.dssSolution.Converged else "Erro")
        time.sleep(0)

    def Solve(self):
        self.dssSolution.Solve()

    def Hour(self, Horas: float = None):
        if Horas is not None:
            self.dssSolution.Hour = Horas
        return self.dssSolution.Hour

    def StepsizeHr(self, passo_h = None):
        if passo_h is not None:
            self.dssSolution.StepsizeHr = passo_h
        # return self.dssSolution.StepsizeHr

    def StepsizeMin(self, passo_min = None):
        if passo_min is not None:
            self.dssSolution.StepsizeMin = passo_min
        # return self.dssSolution.StepsizeMin

    def StepSize(self, passo_sec = None):
        if passo_sec is not None:
            self.dssSolution.StepSize = passo_sec
        return self.dssSolution.StepSize

    def dblHour(self):
        return self.dssSolution.dblHour

    def Number(self, Number: int = None):
        if Number is None:
            return self.dssSolution.Number
        else:
            self.dssSolution.Number = Number
            return self.dssSolution.Number

    def ModeDaily(self):
        self.dssSolution.Mode = SolveModes.dssDaily
        return self.dssSolution.Mode

    def InitSnap(self):
        return self.dssSolution.InitSnap()

    def FinishTimeStep(self):
        return self.dssSolution.FinishTimeStep()

    def SolveNoCOntrol(self):
        return self.dssSolution.SolveNoCOntrol()