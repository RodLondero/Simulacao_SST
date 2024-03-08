# -*- coding: utf-8 -*-

import locale
# Set to German locale to get comma decimal separater
locale.setlocale(locale.LC_NUMERIC, "pt_BR")

import os
import sys
from win32com.client import makepy
import win32com.client
from matplotlib.ticker import (FormatStrFormatter, AutoMinorLocator)
import matplotlib.pyplot as plt

from ClassesDSS.Funcoes import *
from ClassesDSS.Options import *

from matplotlib.font_manager import FontProperties
from ClassesDSS.Loads import Loads
from ClassesDSS.Text import Text
from ClassesDSS.Bus import Bus
from ClassesDSS.Lines import Lines
from ClassesDSS.Circuit import Circuit
from ClassesDSS.Solution import Solution
from ClassesDSS.CktElements import CktElements
from ClassesDSS.Transformers import Transformers
from ClassesDSS.Monitors import Monitors
from ClassesDSS.LineCodes import LineCodes
from ClassesDSS.LoadShapes import LoadShapes

fontP = FontProperties()
fontP.set_size("small")
fontP.set_family('Times New Roman')
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})
plt.rcParams['axes.formatter.use_locale'] = True

class DSS:

    def __init__(self, dssFileName: str):
        """
        :param dssFileName: Caminho completo do arquivo .dss
        """

        self.dssFileName = dssFileName.replace('"', '')

        sys.argv = ["makepy", "OpenDSSEngine.DSS"]
        makepy.main()

        # Criar a conexão entre Python e OpenDSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        # Iniciar o Objeto DSS
        if not self.dssObj.Start(0):
            print("Problemas em iniciar o OpenDSS")
        else:
            # Criar variáveis para as principais interfaces
            self.dssText            = Text(self.dssObj.Text)
            self.dssCircuit         = Circuit(self.dssObj.ActiveCircuit)
            self.dssCktElement      = CktElements(self.dssCircuit.ActiveCktElement(), self.dssObj.ActiveCircuit)
            self.dssBus             = Bus(self.dssObj.ActiveCircuit, self.dssCircuit.ActiveBus())
            self.dssLines           = Lines(self.dssCircuit.Lines())
            self.dssLoads           = Loads(self.dssCircuit.Loads())
            self.dssTransformers    = Transformers(self.dssCircuit.Transformers())
            self.dssMonitors        = Monitors(self.dssCircuit.Monitors())
            self.dssSolution        = Solution(self.dssCircuit.Solution(), self.dssText)
            self.dssLinesCodes      = LineCodes(self.dssCircuit.LineCodes())
            self.dssLoadShapes      = LoadShapes(self.dssCircuit.LoadShapes())

            self.dir_principal      = self.DataPath(self.dssFileName.rstrip(self.dssFileName.split('/')[len(self.dssFileName.split('/'))-1]))
            self.dir_resultados     = self.dir_principal + "Resultados"
            self.dir_plots          = self.dir_principal + "Plots"

    def versao_DSS(self):
        return self.dssObj.Version

    def compila_DSS(self):
        # Limpar informações da última simulação
        self.dssObj.ClearAll()
        self.dssText.Command("Compile " + "\"" + self.dssFileName + "\"")

    def CalcVoltageBases(self, VLinha: list):
        self.dssText.Command("Set Voltagebases=" + str(VLinha))
        # [115, 13.8, '@VL']")
        self.dssText.Command("calcvoltagebases")

    def DataPath(self, diretorio: str = None):
        if diretorio is None:
            return self.dssObj.DataPath
        else:
            self.dssObj.DataPath = diretorio
            return self.dssObj.DataPath

# ======================================================================================================================
#   Geração de arquivos com resultados
# ======================================================================================================================
    def show_powers_kva_elements(self):
        self.DataPath(self.dir_resultados)

        w = os.listdir(self.dir_resultados)
        v = []
        for arq in w:
            n = arq.split('-')
            if n[0].strip() == 'IEEE13BARRAS_Power_elem_kVA':
                v.append(int(n[1].split(".")[0].strip()))

        try:
            idx = w.index('IEEE13BARRAS_Power_elem_kVA.txt')
            nome = w[idx].split('.')[0]
            if v == []:
                novo_v = 1
            else:
                novo_v = v[len(v) - 1] + 1
            os.rename(self.dir_resultados + "/" + w[idx], self.dir_resultados + "/" + nome + " - " + "{:02}".format(novo_v) + ".txt" )

        finally:
            self.dssText.Command("Show Powers KVA Elements")

        self.DataPath(self.dir_principal)

    def show_voltages_LN_elements(self):
        self.DataPath(self.dir_resultados)
        self.dssText.Command("Show Voltage LN Elements")
        self.DataPath(self.dir_principal)

    def Profile(self, config_pu, config_pu_normal):
        for i in config_pu_normal:
            self.dssText.Command("Set {} = {}".format(i, config_pu_normal[i]))
        self.dssText.Command("Plot Profile Phases=Primary")
        for i in config_pu:
            self.dssText.Command("Set {} = {}".format(i, config_pu[i]))

    def get_potencias_elemento(self, Nome_Elemento: list = None):

        for elemento in Nome_Elemento:
            barras = self.dssCktElement.get_barras_elemento(elemento)
            S1, S2 = self.dssCktElement.Powers()

            msg = ("Elemento: " + self.dssCktElement.Name()) + "\n"
            msg = msg + ("{barra:12s} | {fase:^4s} | Potência (kva)".format(barra="Barra", fase="Fase"))
            # msg = msg + ("{:-^33s}".format('-'))
            print(msg)

            terminais = self.dssCktElement.NumTerminals()
            fases = self.dssCktElement.NumPhases()

            for i in range(0, terminais):
                cont = 1

                for j in range(0, fases):
                    if terminais > 1:
                        S_tmp = S1[j] if i == 0 else S2[j]
                    else:
                        S_tmp = S1[j]

                    if S_tmp.__abs__() > 0:
                        # if i == 1 and cont == 1: print()
                        print("{nome:12s} | {fase:^4s} | {s:.4f}".format(nome=barras[i], fase=str(cont),
                                                                        s=S_tmp))

                    cont += 1
        print("{:-^66s}".format('-'))

    def get_tensoes_elemento(self, Nome_Elemento: list):
        print("{:-^66s}".format('-'))
        for elemento in Nome_Elemento:
            barras = self.dssCktElement.get_barras_elemento(elemento)
            tensoes = self.dssCktElement.VoltagesMagAng()

            msg = ("Elemento: " + self.dssCktElement.Name()) + "\n"
            msg = msg + ("{barra:12s} | {fase:^4s} | V(pu) |_ Angº ".format(barra="Barra", fase="Fase"))
            print(msg)

            for i in range(0, len(barras)):
                cont = 1
                if i == 1:
                    print("{:-^55s}".format('-'))

                for j in range(0, len(tensoes[i])):
                    V = tensoes[i][j]
                    Angulo = tensoes[i + 2][j]

                    Vbase = self.dssBus.kVBase(barras[i]) * 1000
                    Vpu = V / Vbase

                    print("{nome:12s} | {fase:^4s} | {v:.4f} ({vpu:.4f})|_ {angulo:.4f}".format(nome=barras[i],
                                                                                                fase=str(cont),
                                                                                                v=V,
                                                                                                vpu=Vpu,
                                                                                                angulo=Angulo))
                    # print("{} - {V:.4f} ({Vpu:.4f})|_ {Angulo:.4f}".format(barras[i], V, Vpu, Angulo))
                    cont += 1
            print("{:-^66s}".format('-'))

# =============================================================================
#   Plots
# =============================================================================
    def Perfil_Tensao(self):
        VA         = list(self.dssCircuit.AllNodeVmagPUByPhase(1))
        DistA      = list(self.dssCircuit.AllNodeDistancesByPhase(1))
        tam = len(DistA)
        DistA[tam - 1] = DistA[tam - 2] if DistA[tam - 1] == 0 else DistA[tam - 1]
        min_dist_A = min(DistA)
        max_dist_A = max(DistA)

        VB         = list(self.dssCircuit.AllNodeVmagPUByPhase(2))
        DistB      = list(self.dssCircuit.AllNodeDistancesByPhase(2))
        tam = len(DistB)
        DistB[tam - 1] = DistB[tam - 2] if DistB[tam - 1] == 0 else DistB[tam - 1]
        min_dist_B = min(DistB)
        max_dist_B = max(DistB)

        VC         = list(self.dssCircuit.AllNodeVmagPUByPhase(3))
        DistC      = list(self.dssCircuit.AllNodeDistancesByPhase(3))
        tam = len(DistC)
        DistC[tam - 1] = DistC[tam - 2] if DistC[tam - 1] == 0 else DistC[tam - 1]

        min_dist_C = min(DistC)
        max_dist_C = max(DistC)
        min_dist = np.min([min_dist_A, min_dist_B, min_dist_C])
        max_dist = np.max([max_dist_A, max_dist_B, max_dist_C]) + 2

        Vmin = np.min(np.min([VA, VB, VC])) - 0.05

        plt.figure()
        # plt.yticks(np.arange(0.8, 1.1, step=y_step / 2))
        plt.subplot(1, 1, 1).set_xlim([min_dist, max_dist])
        plt.subplot(1, 1, 1).set_ylim([Vmin, 1.1])
        plt.title('Perfil de tensão')
        plt.plot([min_dist, max_dist], [0.95, 0.95], 'r')
        plt.plot([min_dist, max_dist], [1.05, 1.05], 'r')
        plt.plot(DistA, VA, 'k', label='VA')
        plt.plot(DistB, VB, 'b', label='VB')
        plt.plot(DistC, VC, 'g', label='VC')
        plt.ylabel('Tensão (pu)')
        plt.xlabel('Distância (km)')
        plt.legend(loc='best', ncol=4,
                   borderaxespad=0, shadow=True, fancybox=True, prop=fontP)

        plt.axes().xaxis.set_minor_locator(AutoMinorLocator(2))
        plt.axes().yaxis.set_minor_locator(AutoMinorLocator(2))
        plt.axes().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.grid(True)
        plt.grid(b=True, which='minor', color='#DCDCDC')
        # plt.annotate("Barra X",
        #              xy=(DistA[2], VA[2]),
        #              xycoords='data',
        #              xytext=(DistA[2]-2.5, VA[2]+0.01),
        #              textcoords='data',
        #              arrowprops=dict(arrowstyle="->", connectionstyle="arc"))

        plt.show()

        return VA, VB, VC, DistA, DistB, DistC

    def Plot_Monitor(self, Nome_Monitor: str, Canais: list, pu: bool = None, Base: float = None, ylim: list = None):
        self.dssMonitors.Name(Nome_Monitor)
        self.dssMonitors.Save()

        V = []
        X = []
        for i in range(0, len(Canais)):
            V_tmp = self.dssMonitors.Channel(Canais[i])
            X_tmp = np.arange(ConfigSimulacao.hora_inicial+1, ConfigSimulacao.hora_inicial + ConfigSimulacao.iteracoes + 1, ConfigSimulacao.passo_simulacao)

            if V.__len__() == 0:
                V = np.array(V_tmp)
                X = np.array(X_tmp)
            else:
                V = np.vstack((V, V_tmp))
                X = np.vstack((X, X_tmp))

        if pu:
            V = V / Base

        Vmin = V.min()
        Vmax = V.max()

        if pu:
            Vmin = np.min((Vmin, 0.92))
            Vmax = np.max((Vmax, 1.05)) + 0.1

        if ylim is not None:
            Vmin = ylim[0]
            Vmax = ylim[1]

        plt.figure()
        plt.gcf().canvas.set_window_title("Monitor {}".format(self.dssMonitors.Name()))

        # plt.subplot(1, 1, 1).set_ylim([Vmin-5, Vmax+5])

        # mx = MultipleLocator(1)
        # my = MultipleLocator((max(V[0]) + min(V[0])) / (2*len(V[0])))


        if len(Canais) > 1:
            for i in range(0, len(V)):
                plt.plot(X[i][:], V[i][:], label="Fase {}".format(i+1))
            if pu:
                plt.plot([0, len(V[0])], [0.92, 0.92], 'r')
                plt.plot([0, len(V[0])], [1.05, 1.05], 'r')
            plt.legend()
        else:
            plt.plot(V)
            if pu:
                plt.plot([0, len(V)], [0.92, 0.92], 'r')
                plt.plot([0, len(V)], [1.05, 1.05], 'r')

        plt.axes().xaxis.set_minor_locator(AutoMinorLocator(2))
        plt.axes().yaxis.set_minor_locator(AutoMinorLocator(2))
        plt.grid(True)
        plt.grid(b=True, which='minor', color='#DCDCDC')
