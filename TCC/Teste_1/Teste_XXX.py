# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:27:50 2018

@author: Rodolfo Londero
"""
import numpy as np
from ClassesDSS.Funcoes import *
from ClassesDSS.DSS import DSS
from matplotlib.ticker import (AutoMinorLocator)
import csv

obj = DSS("E:/Users/Rodolfo/Documentos/OpenDSS/ProjetoSST/Teste_1/Master_SST.dss")
obj.compila_DSS()

# Atalhos para as classes
dssBus = obj.dssBus
dssCktElement = obj.dssCktElement
dssLine = obj.dssLines
dssLoad = obj.dssLoads
dssMonitor = obj.dssMonitors
dssSolution = obj.dssSolution
dssTransformer = obj.dssTransformers

# dssSolution.MaxControlIterations = 100
# dssSolution.MaxControlIterations = 100
# dssSolution.ControlMode = -1
# dssSolution.Number = 24
# dssSolution.Mode = 1
# dssSolution.Hour = 0
# dssSolution.StepsizeHr = 1

obj.dssText.Command("Set Voltagebases=[115, 13.8, '@VL']")
obj.dssText.Command("calcvoltagebases")
dssSolution.Daily(1, 'h', 0, 24)

obj.dssText.Command("Set Voltagebases=[115, 13.8, '@VL']")
obj.dssText.Command("calcvoltagebases")
dssSolution.Daily(1, 'h', 0, 24)

dssMonitor.Name("Potencia_Subestacao")
plt.plot(dssMonitor.Channel(1), label='Rodando direto"')

# p = []
# for i in range(24):
#     obj.dssText.Command("Set Voltagebases=[115, 13.8, '@VL']")
#     obj.dssText.Command("calcvoltagebases")
#     dssSolution.Daily(1, 'h', i, 1)
#     p1, _ = dssCktElement.Powers("VSource.Source")
#     p.append(-p1[0].real)
#
# plt.plot(p, label="Rodando no Loop Calculando VOltageBases")

obj.dssText.Command("Set Voltagebases=[115, 13.8, '@VL']")
obj.dssText.Command("calcvoltagebases")
# dssSolution.Solve()
dssSolution.Daily(1, 'h', 0, 24)

dssMonitor.Name("Potencia_Subestacao")
p = dssMonitor.Channel(1)

plt.plot(p, label="Rodando no Loop Calculando 1x o vOltageBases")
plt.legend()

