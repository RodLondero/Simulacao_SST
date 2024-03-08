# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:27:50 2018

@author: Rodolfo Londero
"""
import numpy as np
import matplotlib.pyplot as plt
from ClassesDSS.DSS import DSS
from ClassesDSS.Funcoes import ControlModes, SolveModes

obj = DSS("E:/Usuário/Documentos/OpenDSS/ProjetoSST/Teste_1/Master.dss")

obj.compila_DSS()
obj.dssSolution.Daily(1, 'h', 24)

print("Sucesso" if obj.dssSolution.Converged() else "Erro")

print('\nAntes de ajustar o tap\n')

print("Elemento ativo: " + obj.dssCktElement.Ativa_Elemento("Transformer.Trafo"))
print("Tap do Enrolamento 1: " + str(obj.dssTransformers.Tap(1)))
print("Tap do Enrolamento 2: " + str(obj.dssTransformers.Tap(2)))


# obj.dssText.Command("Export Summary Sumario1.csv")
# obj.Perfil_Tensao()
obj.Plot_Monitor("Tensao_Carga2", [1, 3, 5], ylim=[150, 220])
obj.dssMonitors.SaveAll()
obj.dssText.Command("Plot monitor object= tensao_carga2 channels=(1 3 5 )")

print('\nApós ajustar o tap\n')

print("Elemento ativo: " + obj.dssCktElement.Ativa_Elemento("Transformer.Trafo"))
print("Tap do Enrolamento 1: " + str(obj.dssTransformers.Tap(1)))
print("Tap do Enrolamento 2: " + str(obj.dssTransformers.Tap(2, 1.05)))

obj.dssSolution.Daily(1, 'h', 24, ControlMode=ControlModes.dssStatic)
print("Sucesso" if obj.dssSolution.Converged() else "Erro")
obj.dssText.Command("Export Summary Sumario2.csv")
# obj.Perfil_Tensao()
obj.dssMonitors.SaveAll()

obj.dssText.Command("Plot monitor object= tensao_carga2 channels=(1 3 5 )")

# print()

# print("Tap do Enrolamento 2: " + str(obj.dssTransformers.Tap(2)))

# obj.dssSolution.Daily(1, 'h', 24)
# obj.dssText.Command("Export Summary Sumario2.csv")
# obj.Perfil_Tensao()
# print(obj.dssSolution.Converged())
# print()
# obj.get_potencias_elemento()

print("Carga: " + obj.dssLoads.set_carga_by_name('Carga2'))
base_kv = obj.dssLoads.kV()
print("Tensão nominal (kV): %.4f" % base_kv)

obj.Plot_Monitor("Tensao_Carga2", [1, 3, 5], ylim=[150, 220])


#obj.dssText.Command("Plot Profile")


#obj.dssText.Command("Transformer.Trafo.Taps = [1.05, 1]")

# obj.dssCktElement.Ativa_Elemento("Transformer.Trafo")
# obj.dssTransformers.set_trafo_by_name("Trafo")
# obj.dssTransformers.Tap(1, 1.1)
# obj.dssSolution.Daily(1, 'h', 24)


# #
# obj.dssCktElement.Ativa_Elemento("Transformer.Trafo")
# obj.dssTransformers.set_trafo_by_name("Trafo")
# obj.dssTransformers.Tap(1, 0.92)
# obj.dssSolution.Daily(1, 'h', 24)
# obj.dssText.Command("Export Summary Sumario3.csv")
# # obj.dssText.Command("plot profile")
# obj.Perfil_Tensao()



# print("Tensões (kV): " + str(obj.dssCktElement.Voltages))
# print("Tensões (pu): " + str(tuple(i/(base_kv*1000) for i in obj.dssCktElement.Voltages)))
#
# obj.plot_perfil_tensao()
#
# # obj.comando_dss('Plot monitor object=tensao_carga channels=(1 3 5 )')
#
# obj.dssTransformers.wdg = 1
# obj.dssTransformers.Tap = 1.5
#
# obj.dssTransformers.wdg = 2
# obj.dssTransformers.Tap = 1
# obj.dssSolution.Solve()
#
# print('\nApós ajustar o tap')
#
# print("Elemento ativo: " + obj.ativa_elemento("Transformer.Trafo"))
# print("Enrolamento 1: " + str(obj.get_tap_terminal_trafo(1)))
# print("Enrolamento 2: " + str(obj.get_tap_terminal_trafo(2)))
#
# print(obj.ativa_elemento('Load.Carga2'))
# base_kv = obj.dssLoads.kV()
# print(base_kv)
#
# print("Tensões (kV): " + str(obj.dssCktElement.Voltages))
# print("Tensões (pu): " + str(tuple(i/(base_kv*1000)
#                                    for i in obj.dssCktElement.Voltages)))
# VA, VB, VC, distA, distB, distC = obj.plot_perfil_tensao()

# obj.comando_dss('Plot monitor object=tensao_carga channels=(1 3 5 )')
