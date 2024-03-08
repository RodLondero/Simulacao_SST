from easygui import *
from ClassesDSS.Plots import *
from ClassesDSS.DSS import *
import numpy as np
import re

obj = DSS("\"E:/Google Drive/Engenharia Elétrica/10º Semestre/TCC/TCC - Rodolfo/Simulação/13Barras/Master.dss\"")

# Atalhos para as classes
dssBus          = obj.dssBus
dssCircuit      = obj.dssCircuit
dssCktElement   = obj.dssCktElement
dssLine         = obj.dssLines
dssLoad         = obj.dssLoads
dssMonitor      = obj.dssMonitors
dssSolution     = obj.dssSolution
dssText         = obj.dssText
dssTransformer  = obj.dssTransformers

try:
    titulo_eixo = titulo_eixo('pt')
except:
    msgBox("Idioma não definido.", 2)
    sys.exit()

# Configurações da simulação
vmaxpu              = 1.05
vminpu              = 0.93
fpmaxpu             = 1
fpminpu             = 0.92
passo_simulacao     = '1m'
hora_inicial        = 0
segundo_inicial     = 0
dias                = 1
horas               = 24 * dias
iteracoes           = horas * 60 if passo_simulacao.find('m') > -1 else horas
range_horas         = range(0, horas)
range_segundos      = range(0, 60*60, 60) if passo_simulacao.find('m') > -1 else range(0, 1)
tempo               = range(1, iteracoes+1)
plots               = []
figuras             = []
tamanho_figuras_sep = (7, 3.5)
tamanho_figuras_jun = (7, 7)
fase                = ['A', 'B', 'C']

config_pu        = {'emergvminpu': 0.7, 'emergvmaxpu': 1.2, 'normvminpu': 0.80, 'normvmaxpu': 1.10}
config_pu_normal = {'emergvminpu': 0.8, 'emergvmaxpu': 1.1, 'normvminpu': 0.95, 'normvmaxpu': 1.05}

obj.compila_DSS()
obj.CalcVoltageBases([115, 4.16, 0.38])
# ---------------------------------------------------------------------------------------------------------------------#
# Funções
# ---------------------------------------------------------------------------------------------------------------------#
# Executa comandos no OpenDSS
def comando(text: str):
    dssText.Command(text)

# Define se utiliza SST ou TR
def define_simulacao_com_sst(usa_sst: bool):
    # sst = [633, 645, 692, 684]
    sst = [633, 645]
    for SST in sst:
        dssCktElement.Enabled("VSource.FonteSST_" + str(SST),           usa_sst)
        dssCktElement.Enabled("Monitor.Potencia_FonteSST_" + str(SST),  usa_sst)
        dssCktElement.Enabled("Load.CargaSST_" + str(SST),              usa_sst)
        dssCktElement.Enabled("Transformer.TR" + str(SST),          not usa_sst)

def adiciona_sst(tr: list):
    comando_cargas = []
    comando_fontes = []
    comando_monitores = []
    nomes_cargas_sst = []
    nomes_fontes_sst = []

    for i in tr:
        nome = dssTransformer.Name(i)
        if dssCktElement.Enabled("Transformer." + nome):
            phases = dssCktElement.NumPhases()
            barra_MT = dssCktElement.get_barras_elemento()[0]
            barra_BT = dssCktElement.get_barras_elemento()[1]
            kv_MT = dssTransformer.kV(1)
            kv_BT = dssTransformer.kV(2)

            j = dssLoad.First()

            while j:
                nome_carga = dssLoad.Name()
                if dssCktElement.Enabled("Load." + nome_carga):
                    if dssCktElement.get_barras_elemento()[0] in [barra_BT, barra_BT + ".1", barra_BT + ".2",
                                                                  barra_BT + ".3", barra_BT + '.1.2.3',
                                                                  barra_BT + '.1.2', barra_BT + '.2.3',
                                                                  barra_BT + '.1.3']:

                        nomes_cargas_sst.append("CargaSST_" + nome_carga)
                        nomes_fontes_sst.append("FonteSST_" + nome_carga)
                        barra_fonte = dssCktElement.get_barras_elemento()[0]
                        barra_carga = barra_fonte.replace(barra_BT, barra_MT)

                        conn = 'Delta ' if dssLoad.IsDelta() else 'Wye '
                        loadshape = "Unitario_Minutos" if passo_simulacao.find('m') > -1 else "Unitario_Horas"
                        tensao = str(kv_MT / np.sqrt(3)) if dssCktElement.NumPhases() == 1 else str(kv_MT)
                        cmd  = 'New Load.CargaSST_' + nome_carga
                        cmd += ' Bus1 = ' + barra_carga
                        cmd += ' Phases = ' + str(dssCktElement.NumPhases())
                        cmd += ' Conn = ' + 'Delta'
                        cmd += ' Model = 1  '
                        cmd += ' kV = ' + tensao
                        cmd += ' kw = ' + str(dssLoad.kW())
                        cmd += ' kvar= ' + str(dssLoad.kvar())
                        cmd += ' daily = ' + loadshape

                        comando_cargas.append(cmd)

                        cmd = 'New VSource.FonteSST_' + nome_carga
                        cmd += ' Bus1 = ' + barra_fonte
                        cmd += ' Phases = ' + str(dssCktElement.NumPhases())
                        cmd += ' basekV = ' + str(dssLoad.kV())

                        comando_fontes.append(cmd)

                        comando_monitores.append('New Monitor.Potencia_FonteSST_{} element = VSource.FonteSST_{} '
                                                 'terminal = 1 mode = 1 ppolar = no'.format(nome_carga, nome_carga))
                        comando_monitores.append('New Monitor.Tensao_FonteSST_{} element = VSource.FonteSST_{} '
                                                 'terminal = 1 mode = 0 ppolar = no'.format(nome_carga, nome_carga))
                        comando_monitores.append('New Monitor.Potencia_CargaSST_{} element = Load.CargaSST_{}    '
                                                 'terminal = 1 mode = 1 ppolar = no'.format(nome_carga, nome_carga))
                        comando_monitores.append('New Monitor.Tensao_CargaSST_{} element = Load.CargaSST_{}    '
                                                 'terminal = 1 mode = 0 ppolar = no'.format(nome_carga, nome_carga))
                j = dssLoad.Next()

        dssCktElement.Enabled("Transformer." + nome, False)

    if len(comando_cargas) > 0:
        for cmd in comando_cargas:
            comando(cmd)
    if len(comando_fontes) > 0:
        for cmd in comando_fontes:
            comando(cmd)
    if len(comando_monitores) > 0:
        for cmd in comando_monitores:
            comando(cmd)

    return nomes_cargas_sst, nomes_fontes_sst

def define_LoadsLimitsPU(minimo, maximo):
    i = dssLoad.First()
    while i:
        dssLoad.vminpu(minimo)
        dssLoad.vmaxpu(maximo)
        i = dssLoad.Next()

def define_LoadShapes(LoadShape: str):
    i = dssLoad.First()
    while i:
        dssLoad.daily(LoadShape)
        i = dssLoad.Next()

def getBase(Nome_Elemento: str, terminal: int = 1):
    return dssBus.kVBase(dssCktElement.get_barras_elemento(Nome_Elemento)[terminal]) * 1000

def plotar_subestacao_P(fases_juntas: bool, teste: int, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # P Subestação
    ax = []
    if fases_juntas:
        fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
        ax = axes

    if fases_juntas:
        fig.gca().name = "Teste_{:02d}_Subestacao_P".format(teste)
        plt.gcf().canvas.set_window_title(fig.gca().name)

    for i in range(0, 3):
        if not fases_juntas:
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
            ax.append(axes)
            fig.gca().name = "Teste_{:02d}_Subestacao_P_{}".format(teste, fase[i])
            plt.gcf().canvas.set_window_title(fig.gca().name)

        p_sst = [-p for p in subestacao_P_SST[i]]
        p_tr  = [-p for p in subestacao_P_TR[i]]

        ax[i].set_xlabel(titulo_eixo.tempo)
        ax[i].set_ylabel(titulo_eixo.subestacao_P)
        ax[i].plot(tempo, p_tr, label="Com TR (Fase {})".format(fase[i]), linewidth=1)
        ax[i].plot(tempo, p_sst, label="Com SST (Fase {})".format(fase[i]), linewidth=1)

        minimo = min(min(p_tr), min(p_sst))
        if minimo < 0:
            minimo = minimo * 1.1
        else:
            minimo = minimo * 1.1
        maximo = 100

        ax[i].set_ylim([minimo, maximo])
        ax[i].legend(loc='lower left', fontsize='small', ncol=3, labelspacing=0,
                     columnspacing=0.5, handlelength=1, handletextpad=0.3)
        plt.tight_layout()

        # figura_subestacao_P.append(fig)
        # plot_subestacao_P.append(ax)

def plotar_subestacao_Q(fases_juntas: bool, teste: int, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # P Subestação
    ax = []
    if fases_juntas:
        fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
        ax = axes

    if fases_juntas:
        fig.gca().name = "Teste_{:02d}_Subestacao_Q".format(teste)
        plt.gcf().canvas.set_window_title(fig.gca().name)

    for i in range(0, 3):
        if not fases_juntas:
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
            ax.append(axes)
            fig.gca().name = "Teste_{:02d}_Subestacao_Q_{}".format(teste, fase[i])
            plt.gcf().canvas.set_window_title(fig.gca().name)

        q_tr = [-q for q in subestacao_Q_TR[i]]
        q_sst = [-q for q in subestacao_Q_SST[i]]

        ax[i].set_xlabel(titulo_eixo.tempo)
        ax[i].set_ylabel(titulo_eixo.subestacao_Q)
        ax[i].plot(tempo, q_tr, label="Com TR (Fase {})".format(fase[i]), linewidth=1)
        ax[i].plot(tempo, q_sst, label="Com SST (Fase {})".format(fase[i]), linewidth=1)

        minimo = min(min(q_tr), min(q_sst))
        if minimo < 0:
            minimo = minimo * 1.1
        else:
            minimo = minimo * 0.1
        maximo = 300

        ax[i].set_ylim([minimo, maximo])
        ax[i].legend(loc='lower left', fontsize='small', ncol=3, labelspacing=0,
                     columnspacing=0.5, handlelength=1, handletextpad=0.3)
        plt.tight_layout()

        # figura_subestacao_Q.append(fig)
        # plot_subestacao_Q.append(ax)

def plotar_subestacao_FP(fases_juntas: bool, teste, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # FP Subestação
    ax = []
    if fases_juntas:
        fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
        ax = axes

    if fases_juntas:
        fig.gca().name = "Teste_{:02d}_Subestacao_FP".format(teste)
        plt.gcf().canvas.set_window_title(fig.gca().name)

    for i in range(0, 3):
        if not fases_juntas:
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
            ax.append(axes)
            fig.gca().name = "Teste_{:02d}_Subestacao_FP_{}".format(teste, fase[i])
            plt.gcf().canvas.set_window_title(fig.gca().name)
        ax[i].set_xlabel(titulo_eixo.tempo)
        ax[i].set_ylabel(titulo_eixo.subestacao_FP)
        ax[i].plot(tempo, calculaFP(subestacao_P_TR[i], subestacao_Q_TR[i]), label="Com TR (Fase {})".format(fase[i]), linewidth=1)
        ax[i].plot(tempo, calculaFP(subestacao_P_SST[i], subestacao_Q_SST[i]), label="Com SST (Fase {})".format(fase[i]), linewidth=1)

        plot_limites(ax[i], fpminpu, fpmaxpu, iteracoes)

        ax[i].legend(loc='best', fontsize='small', ncol=3, labelspacing=0,
                  columnspacing=0.5, handlelength=1, handletextpad=0.3)
        plt.tight_layout()

def plotar_cargas_V_BT(fases_juntas: bool, teste, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # Tensões BT nas cargas
    for carga in Cargas:

        letra = re.sub('[^a-z]', '', carga)
        if letra in ['a', 'b', 'c']:
            letra = letra.upper()

        ax = []
        dssCktElement.Ativa_Elemento("Load." + carga)
        if dssCktElement.NumPhases() == 3 and fases_juntas:
            fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
            ax = axes
            fig.gca().name = "Teste_{:02d}_Carga_{}_V_BT".format(teste, carga)
            plt.gcf().canvas.set_window_title(fig.gca().name)
        for i in range(0, 3):
            if sum(carga_V_BT_TR[carga][i][0]) > 0:
                f = letra
                if f == '':
                    f = fase[i]

                if (dssCktElement.NumPhases() != 3 and fases_juntas) or (not fases_juntas):
                    fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
                    ax.append(axes)
                    fig.gca().name = "Teste_{:02d}_Carga_{}_V_BT_{}".format(teste, carga, f)
                    plt.gcf().canvas.set_window_title(fig.gca().name)

                ax[i].set_xlabel(titulo_eixo.tempo)
                ax[i].set_ylabel(titulo_eixo.carga_V)
                ax[i].plot(tempo, carga_V_BT_TR[carga][i][1], label="Com TR (Fase {})".format(f), linewidth=1)
                ax[i].plot(tempo, carga_V_BT_SST[carga][i][1], label="Com SST (Fase {})".format(f), linewidth=1)

                plot_limites(ax[i], vminpu, vmaxpu, iteracoes)

                ax[i].legend(loc='upper left', fontsize='small', ncol=3, labelspacing=0,
                          columnspacing=0.5, handlelength=1, handletextpad=0.3)
                plt.tight_layout()
                
def plotar_cargas_V_MT(fases_juntas: bool, teste, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # Tensões MT nas cargas
    for carga in Cargas:

        letra = re.sub('[^a-z]', '', carga)
        if letra in ['a', 'b', 'c']:
            letra = letra.upper()

        ax = []
        dssCktElement.Ativa_Elemento("Load." + carga)
        if dssCktElement.NumPhases() == 3 and fases_juntas:
            fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
            ax = axes
            fig.gca().name = "Teste_{:02d}_Carga_{}_V_MT".format(teste, carga)
            plt.gcf().canvas.set_window_title(fig.gca().name)

        for i in range(0, 3):
            if sum(carga_V_MT_TR[carga][i][0]) > 0:
                f = letra
                if f == '':
                    f = fase[i]

                if (dssCktElement.NumPhases() != 3 and fases_juntas) or (not fases_juntas):
                    fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
                    ax.append(axes)
                    fig.gca().name = "Teste_{:02d}_Carga_{}_V_MT_{}".format(teste, carga, f)
                    plt.gcf().canvas.set_window_title(fig.gca().name)

                ax[i].set_xlabel(titulo_eixo.tempo)
                ax[i].set_ylabel(titulo_eixo.carga_V)
                ax[i].plot(tempo, carga_V_MT_TR[carga][i][1], label="Com TR (Fase {})".format(f), linewidth=1)
                ax[i].plot(tempo, carga_V_MT_SST[carga][i][1], label="Com SST (Fase {})".format(f), linewidth=1)

                plot_limites(ax[i], vminpu, vmaxpu, iteracoes)

                ax[i].legend(loc='best', fontsize='small', ncol=3, labelspacing=0,
                          columnspacing=0.5, handlelength=1, handletextpad=0.3)
                plt.tight_layout()

def plotar_cargas_P(fases_juntas: bool, teste, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # P cargas
    for carga in Cargas:

        letra = re.sub('[^a-z]', '', carga)
        if letra in ['a', 'b', 'c']:
            letra = letra.upper()

        ax = []
        dssCktElement.Ativa_Elemento("Load." + carga)
        if dssCktElement.NumPhases() == 3 and fases_juntas:
            fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
            ax = axes
            fig.gca().name = "Teste_{:02d}_Carga_{}_P".format(teste, carga)
            plt.gcf().canvas.set_window_title(fig.gca().name)

        for i in range(0, 3):
            if sum(carga_P_TR[carga][i]) > 0:

                f = letra
                if f == '':
                    f = fase[i]

                if (dssCktElement.NumPhases() != 3 and fases_juntas) or (not fases_juntas):
                    fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
                    ax.append(axes)
                    fig.gca().name = "Teste_{:02d}_Carga_{}_P_{}".format(teste, carga, f)
                    plt.gcf().canvas.set_window_title(fig.gca().name)

                ax[i].set_xlabel(titulo_eixo.tempo)
                ax[i].set_ylabel(titulo_eixo.carga_P)
                ax[i].plot(tempo, carga_P_TR[carga][i],  label="Com TR (Fase {})".format(f), linewidth=1)
                ax[i].plot(tempo, carga_P_SST[carga][i], label="Com SST (Fase {})".format(f), linewidth=1)

                minimo = min(min(carga_P_TR[carga][i]), min(carga_P_SST[carga][i]))
                if minimo < 0:
                    minimo = minimo * 1.1
                else:
                    minimo = minimo * 0.1
                maximo = max(max(carga_P_TR[carga][i]), max(carga_P_SST[carga][i])) * 1.1

                ax[i].set_ylim([minimo, maximo])

                ax[i].legend(loc='upper left', fontsize='small', ncol=3, labelspacing=0,
                          columnspacing=0.5, handlelength=1, handletextpad=0.3)
                plt.tight_layout()

def plotar_cargas_Q(fases_juntas: bool, teste, tamanho_figura_jun: tuple, tamanho_figura_sep: tuple):
    # P cargas
    for carga in Cargas:

        letra = re.sub('[^a-z]', '', carga)
        if letra in ['a', 'b', 'c']:
            letra = letra.upper()

        ax = []
        dssCktElement.Ativa_Elemento("Load." + carga)
        if dssCktElement.NumPhases() == 3 and fases_juntas:
            fig, axes = plt.subplots(3, 1, figsize=tamanho_figura_jun)
            ax = axes
            fig.gca().name = "Teste_{:02d}_Carga_{}_Q".format(teste, carga)
            plt.gcf().canvas.set_window_title(fig.gca().name)

        for i in range(0, 3):
            if sum(carga_Q_TR[carga][i]) > 0:

                f = letra
                if f == '':
                    f = fase[i]

                if (dssCktElement.NumPhases() != 3 and fases_juntas) or (not fases_juntas):
                    fig, axes = plt.subplots(1, 1, figsize=tamanho_figura_sep)
                    ax.append(axes)
                    fig.gca().name = "Teste_{:02d}_Carga_{}_Q_{}".format(teste, carga, f)
                    plt.gcf().canvas.set_window_title(fig.gca().name)

                ax[i].set_xlabel(titulo_eixo.tempo)
                ax[i].set_ylabel(titulo_eixo.carga_Q)
                ax[i].plot(tempo, carga_Q_TR[carga][i],  label="Com TR (Fase {})".format(f), linewidth=1)
                ax[i].plot(tempo, carga_Q_SST[carga][i], label="Com SST (Fase {})".format(f), linewidth=1)

                # minimo = min(min(carga_Q_TR[carga][i]), min(carga_Q_SST[carga][i]))
                # if minimo <= 0:
                #     minimo = minimo * 0.1 - 10
                # else:
                #     minimo = minimo * 1.5
                #
                # maximo = max(max(carga_Q_TR[carga][i]), max(carga_Q_SST[carga][i])) * 1.1
                #
                # ax[i].set_ylim([minimo, maximo])

                ax[i].legend(loc='upper left', fontsize='small', ncol=3, labelspacing=0,
                          columnspacing=0.5, handlelength=1, handletextpad=0.3)
                plt.tight_layout()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#                                       SIMULAÇÃO USANDO TR
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
define_LoadsLimitsPU(0.8, 1.1)
define_LoadShapes("Residencial_Minuto" if passo_simulacao.find('m') > -1 else "Residencial")

# ---------------------------------------------------- #
# Escolha dos TRs e Cargas                             #
# ---------------------------------------------------- #
TRs   = ["TR634", "TR645", "TR671"]
Cargas = ['634a', '634b', '634c', '645', '671']
# ---------------------------------------------------- #
carga_V_BT_TR    = {}
carga_V_MT_TR    = {}
carga_P_TR       = {}
carga_Q_TR       = {}

for carga in Cargas:
    carga_V_BT_TR[carga] = [zeros(2, iteracoes), zeros(2, iteracoes), zeros(2, iteracoes)]
    carga_V_MT_TR[carga] = [zeros(2, iteracoes), zeros(2, iteracoes), zeros(2, iteracoes)]
    carga_P_TR[carga]    = zeros(3, iteracoes)
    carga_Q_TR[carga]    = zeros(3, iteracoes)
# ---------------------------------------------------- #
# Solve
dssSolution.Daily(passo_simulacao, (hora_inicial, segundo_inicial), iteracoes)
# ---------------------------------------------------- #
# Obtenção dos dados
# ---------------------------------------------------- #
# Potência ativa, reativa e fator de potência da subestação
subestacao_P_TR  = dssMonitor.getDados("Subestacao_Potencia", [1, 3, 5])
subestacao_Q_TR  = dssMonitor.getDados("Subestacao_Potencia", [2, 4, 6])
subestacao_FP_TR = [calculaFP(subestacao_P_TR[0], subestacao_Q_TR[0]),
                    calculaFP(subestacao_P_TR[1], subestacao_Q_TR[1]),
                    calculaFP(subestacao_P_TR[2], subestacao_Q_TR[2])]

for carga in Cargas:
    basekV_BT = getBase("Load." + carga, 0)
    basekV_MT = getBase("Transformer." + 'TR'+re.sub('[^0-9]', '', carga), 0)
    letra = re.sub('[^a-z]', '', carga)
    dssCktElement.Ativa_Elemento("Load." + carga)
    fases = dssCktElement.NumPhases()
    cont = 1
    canal = 1
    canal_mt = 1
    while cont <= fases:
        # Tensões da carga em BT ------> [0] = kV, [1] = pu
        carga_V_BT_TR[carga][cont-1][0] = dssMonitor.getDados(carga+"_Tensao",    canal)
        carga_V_BT_TR[carga][cont-1][1] = dssMonitor.getDados(carga+"_Tensao",    canal, basekV_BT)

        if fases == 1:
            if letra == 'b':
                canal_mt = 3
            elif letra == 'c':
                canal_mt = 5

        # Tensões da carga em MT ------> [0] = kV, [1] = pu
        carga_V_MT_TR[carga][cont-1][0] = dssMonitor.getDados(carga+"_Tensao_MT", canal_mt)
        carga_V_MT_TR[carga][cont-1][1] = dssMonitor.getDados(carga+"_Tensao_MT", canal_mt, basekV_MT)

        # Potência Ativa e Reativa da carga
        carga_P_TR[carga][cont-1] = dssMonitor.getDados(carga+"_Potencia",   canal)
        carga_Q_TR[carga][cont-1] = dssMonitor.getDados(carga + "_Potencia", canal+1)

        canal += 2
        if fases == 3:
            canal_mt += 2
        cont += 1

# obj.Profile(config_pu=config_pu, config_pu_normal=config_pu_normal)

sleep(0.5)




# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#                                       SIMULAÇÃO USANDO SST
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
nomes_cargas_sst, nomes_fontes_sst = adiciona_sst(TRs)

define_LoadsLimitsPU(0.8, 1.1)
alpha_default = 15

carga_V_BT_SST    = {}
carga_V_MT_SST    = {}
carga_P_SST       = {}
carga_Q_SST       = {}

for carga in Cargas:
    carga_V_BT_SST[carga] = [zeros(2, iteracoes), zeros(2, iteracoes), zeros(2, iteracoes)]
    carga_V_MT_SST[carga] = [zeros(2, iteracoes), zeros(2, iteracoes), zeros(2, iteracoes)]
    carga_P_SST[carga]    = zeros(3, iteracoes)
    carga_Q_SST[carga]    = zeros(3, iteracoes)

subestacao_P_SST  = zeros(3, iteracoes)
subestacao_Q_SST  = zeros(3, iteracoes)
subestacao_FP_SST = zeros(3, iteracoes)

P_vsource_SST = {}
for fonte in nomes_fontes_sst:
    P_vsource_SST[fonte] = zeros(1, iteracoes)

# -------------------------------------------------------------- #
# Obtém a Potência Aparente máxima dos TRs para restrição do SST
# -------------------------------------------------------------- #
base_sst_kva = []
for carga in Cargas:
    dssTransformer.Name('TR'+re.sub('[^0-9]', '', carga))
    base_sst_kva.append(dssTransformer.kva(1))

# -------------------------------------------------------------- #
# Zera a potência reativa nominal dos SSTs
# -------------------------------------------------------------- #
p_sst = {}
for sst in nomes_cargas_sst:
    dssLoad.Name(sst)
    dssLoad.kvar(0)
    p_sst[sst] = []
# -------------------------------------------------------------- #
# Loop das horas e controle
# -------------------------------------------------------------- #
cont = 0
for hora in range_horas:

    for segundo in range_segundos:
        if segundo % 60 == 0:
            print('{}:{}'.format(hora, segundo/60))
        alpha = []

        dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

        # Obtém os dados da atuais e atualiza o SST --------------------------------
        for i in range(0, len(nomes_cargas_sst)):
            alpha.append(alpha_default)

            p1, _ = dssCktElement.Powers("VSource." + nomes_fontes_sst[i])
            P_vsource_SST[nomes_fontes_sst[i]][0][cont] = -p1[0].real

            dssCktElement.Ativa_Elemento("Load." + nomes_cargas_sst[i])
            dssLoad.Name(nomes_cargas_sst[i])
            dssLoad.kW(-p1[0].real * dssCktElement.NumPhases())
            dssLoad.kvar(0)

        dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

        # Percorrer todos os SSTs --------------------------------------------------
        for i in range(0, len(nomes_cargas_sst)):
            v1, _, _, _ = dssCktElement.VoltagesMagAng("Load." + nomes_cargas_sst[i])
            v_min = min([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])
            v_max = max([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])

            ok_vmin = False
            ok_vmax = False

            while (not ok_vmin) and (not ok_vmax):
                # --------------------------------------------------------------------
                # Controle da tensão mínima
                # --------------------------------------------------------------------
                if vminpu > v_min > 0:
                    kva_sst = 0
                    kvar_1 = 0
                    while (v_min < 0.935) and (kva_sst < 1):
                        # kvar_1 = dssLoad.kvar()
                        kvar_1 -= alpha[i]
                        dssLoad.Name(nomes_cargas_sst[i])

                        kw = dssLoad.kW() / base_sst_kva[i]
                        kvar = kvar_1 / base_sst_kva[i]
                        kva_sst = abs(complex(kw, kvar))

                        # p_sst[nomes_cargas_sst[i]].append(kva_sst)

                        # kva_sst_arr.append(kva_sst)

                        if kva_sst < 1:
                            dssLoad.kvar(kvar_1)
                            dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

                            v1, _, _, _ = dssCktElement.VoltagesMagAng("Load." + nomes_cargas_sst[i])
                            v_min = min([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])
                            v_max = max([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])
                        else:
                            print(nomes_cargas_sst[i] + " Saturou no controle do Vmin")
                    # obj.show_powers_kva_elements()

                ok_vmin = True
                # ----------------------------------------------------------------------
                # Controle da tensão máxima
                # ----------------------------------------------------------------------
                if v_max > vmaxpu and v_max > 0:
                    kva_sst = 0
                    kvar_1 = 0
                    while (v_max > vmaxpu) and (kva_sst < 1):
                        kvar_1 = dssLoad.kvar()
                        kvar_1 += alpha[i]

                        dssLoad.Name(nomes_cargas_sst[i])
                        kw = dssLoad.kW() / base_sst_kva[i]
                        kvar = kvar_1 / base_sst_kva[i]

                        kva_sst = abs(complex(kw, kvar))
                        # p_sst[nomes_cargas_sst[i]].append(kva_sst)

                        if kva_sst < 1:
                            dssLoad.kvar(kvar_1)
                            dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

                            v1, _, _, _ = dssCktElement.VoltagesMagAng("Load." + nomes_cargas_sst[i])
                            v_max = max([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])
                        else:
                            print(nomes_cargas_sst[i] + " Saturou no controle do Vmax")
                ok_vmax = True

        # ---------------------------------------------------------------------
        # Correção do FP
        # ---------------------------------------------------------------------
        p, _ = dssCktElement.Powers("VSource.Source")

        for p_i in range(0, len(p)):
            fp_tmp = abs(calculaFP(p[p_i].real, p[p_i].imag))

            if fp_tmp < fpminpu:  # and (fp_tmp > 0.1):
                kvar_1 = 0
                primeiro = 0
                soma = False
                kva_sst = zeros(len(nomes_cargas_sst))
                # while (fp_tmp < fpminpu) and (sum(kva_sst) < len(nomes_cargas_sst)) and (v_max > vmaxpu) and(v_min < 0.935) and (kva_sst < 1):
                while (fp_tmp < fpminpu) and (sum(kva_sst) < len(nomes_cargas_sst)):
                    q = -p[p_i].imag

                    if abs(q) < 1:
                        alpha = 0.01

                    if (q < 0) and (primeiro == 0):
                        soma = True
                    if (q > 0) and (primeiro == 0):
                        soma = False

                    # kvar_1 = dssLoad.kvar()
                    if soma:
                        kvar_1 += alpha_default
                    else:
                        kvar_1 -= alpha_default

                    primeiro = 1

                    # if abs(p.real) < 0.5:
                    #     kvar_1 = np.tan(np.arccos(fpminpu)) * p.real
                    for i in range(0, len(nomes_cargas_sst)):
                        dssLoad.Name(nomes_cargas_sst[i])

                        kw = dssLoad.kW() / base_sst_kva[i]
                        kvar = kvar_1 / base_sst_kva[i]

                        kva_sst[i] = abs(complex(kw, kvar))
                        # kva_sst_arr.append(kva_sst)
                        if kva_sst[i] < 1:
                            dssLoad.kvar(kvar_1)
                        else:
                            print(nomes_cargas_sst[i] + " Saturou no controle do FP")

                    dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

                    p, q = dssCktElement.Powers("VSource.Source")
                    fp_tmp = abs(calculaFP(p[p_i].real, p[p_i].imag))

                    # v1, _, _, _ = dssCktElement.VoltagesMagAng("Load." + nomes_cargas_sst[i])
                    # v_min = min([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])
                    # v_max = max([x / getBase("Load." + nomes_cargas_sst[i], 0) for x in v1])

            dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

         # Coleta de resultados -----------------------------------------------------
        for i in range(0, len(nomes_cargas_sst)):
            dssLoad.Name(nomes_cargas_sst[i])

            kw = dssLoad.kW() / base_sst_kva[i]
            kvar = dssLoad.kvar() / base_sst_kva[i]
            s = abs(complex(kw, kvar))
            p_sst[nomes_cargas_sst[i]].append(s)


        p1, _ = dssCktElement.Powers("VSource.Source")
        subestacao_P_SST[0][cont] = -p1[0].real
        subestacao_P_SST[1][cont] = -p1[1].real
        subestacao_P_SST[2][cont] = -p1[2].real

        subestacao_Q_SST[0][cont] = -p1[0].imag
        subestacao_Q_SST[1][cont] = -p1[1].imag
        subestacao_Q_SST[2][cont] = -p1[2].imag

        for carga in Cargas:
            basekV_BT = getBase("Load." + carga, 0)
            basekV_MT = getBase("Transformer." + 'TR' + re.sub('[^0-9]', '', carga), 0)
            letra = re.sub('[^a-z]', '', carga)
            dssCktElement.Ativa_Elemento("Load." + carga)
            fases = dssCktElement.NumPhases()
            c = 1
            canal = 1
            canal_mt = 1

            while c <= fases:
                # Tensões da carga em BT ------> [0] = kV, [1] = pu
                v1, _, _, _ = dssCktElement.VoltagesMagAng("Load." + carga)

                carga_V_BT_SST[carga][c - 1][0][cont] = v1[c-1]
                carga_V_BT_SST[carga][c - 1][1][cont] = v1[c-1] / basekV_BT

                if fases == 1:
                    if letra == 'b':
                        canal_mt = 3
                    elif letra == 'c':
                        canal_mt = 5

                # Tensões da carga em MT ------> [0] = kV, [1] = pu
                v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.CargaSST_" + carga)
                carga_V_MT_SST[carga][c - 1][0][cont] = v1[c - 1]
                carga_V_MT_SST[carga][c - 1][1][cont] = v1[c - 1] / basekV_MT

                # Potência Ativa e Reativa da carga
                p1, _ = dssCktElement.Powers("Load.CargaSST_" + carga)
                carga_P_SST[carga][c - 1][cont] = p1[c-1].real
                carga_Q_SST[carga][c - 1][cont] = p1[c-1].imag

                canal += 2
                if fases == 3:
                    canal_mt += 2
                c += 1

        cont += 1

# ---------------------------------------------------------------------------------------------------------------------
# Plotagem
# ---------------------------------------------------------------------------------------------------------------------
teste = 4
figura_subestacao_P = []
plot_subestacao_P   = []

if msgSimNao("Plotagem", "Deseja plotar os gráficos?"):
    arquivos = multchoicebox("Escolha os gráficos que deseja salvar", "Escolha", ['Subestação P', 'Subestação Q',
                                                                                  'Subestação FP', 'Cargas V BT',
                                                                                  'Cargas V MT', 'Cargas P', 'Cargas Q'])
    if arquivos is not None:
        opcao = msgSimNao("Forma", "Plotar fases juntas?")
        if 'Subestação P'  in arquivos: plotar_subestacao_P(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)
        if 'Subestação Q'  in arquivos: plotar_subestacao_Q(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)
        if 'Subestação FP' in arquivos: plotar_subestacao_FP(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)
        if 'Cargas V BT'   in arquivos: plotar_cargas_V_BT(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)
        if 'Cargas V MT'   in arquivos: plotar_cargas_V_MT(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)
        if 'Cargas P'      in arquivos: plotar_cargas_P(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)
        if 'Cargas Q'      in arquivos: plotar_cargas_Q(opcao, teste, tamanho_figuras_jun, tamanho_figuras_sep)

        if opcao:
            # TENSAO BT - 634 ----------------------------------------------------
            plt.rcParams.update({'font.size': 12})
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figuras_sep)
            fig.gca().name = "Teste_{:02d}_Carga_634_V_BT".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes.set_xlabel(titulo_eixo.tempo)
            axes.set_ylabel(titulo_eixo.carga_V)
            axes.plot(tempo, carga_V_BT_TR[Cargas[0]][0][1], label='Com TR (Fase A)')
            # axes.plot(tempo, carga_V_BT_SST[Cargas[0]][0][1], label='Com SST (Fase A)')
            axes.plot(tempo, carga_V_BT_TR[Cargas[1]][0][1], label='Com TR (Fase B)')
            # axes.plot(tempo, carga_V_BT_SST[Cargas[1]][0][1], label='Com SST (Fase B)')
            axes.plot(tempo, carga_V_BT_TR[Cargas[2]][0][1], label='Com TR (Fase C)')
            axes.plot(tempo, carga_V_BT_SST[Cargas[2]][0][1], label='Com SST (Fases A, B e C)', color="#924C39")
            axes.legend(loc='upper left', fontsize='small', ncol=1, labelspacing=0.15,
                         columnspacing=0.5, handlelength=1, handletextpad=0.3, bbox_to_anchor=(0, 0.36, 0, 0))
            plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # TENSAO BT - 645 ----------------------------------------------------
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figuras_sep)
            fig.gca().name = "Teste_{:02d}_Carga_645_V_BT".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes.set_xlabel(titulo_eixo.tempo)
            axes.set_ylabel(titulo_eixo.carga_V)
            axes.plot(tempo, carga_V_BT_TR[Cargas[3]][0][1], label='Com TR')
            axes.plot(tempo, carga_V_BT_SST[Cargas[3]][0][1], label='Com SST', color="#924C39")
            axes.legend(loc='upper left', fontsize='small', ncol=2, labelspacing=0.1,
                        columnspacing=0.5, handlelength=1, handletextpad=0.3, bbox_to_anchor=(0, 0.95, 0, 0))
            plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # TENSAO MT - 645 ----------------------------------------------------
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figuras_sep)
            fig.gca().name = "Teste_{:02d}_Carga_645_V_MT".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes.set_xlabel(titulo_eixo.tempo)
            axes.set_ylabel(titulo_eixo.carga_V)
            axes.plot(tempo, carga_V_MT_TR[Cargas[3]][0][1], label='Com TR')
            axes.plot(tempo, carga_V_MT_SST[Cargas[3]][0][1], label='Com SST')
            axes.legend(loc='upper left', fontsize='small', ncol=2, labelspacing=0.1,
                        columnspacing=0.5, handlelength=1, handletextpad=0.3, bbox_to_anchor=(0, 0.95, 0, 0))
            plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # TENSAO BT - 671 ----------------------------------------------------
            fig, axes = plt.subplots(1, 1, figsize=tamanho_figuras_sep)
            fig.gca().name = "Teste_{:02d}_Carga_671_V_BT".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes.set_xlabel(titulo_eixo.tempo)
            axes.set_ylabel(titulo_eixo.carga_V)
            axes.plot(tempo, carga_V_BT_TR[Cargas[4]][0][1], label='Com TR (Fase A)')
            # axes.plot(tempo, carga_V_BT_SST[Cargas[0]][0][1], label='Com SST (Fase A)')
            axes.plot(tempo, carga_V_BT_TR[Cargas[4]][1][1], label='Com TR (Fase B)')
            # axes.plot(tempo, carga_V_BT_SST[Cargas[1]][0][1], label='Com SST (Fase B)')
            axes.plot(tempo, carga_V_BT_TR[Cargas[4]][2][1], label='Com TR (Fase C)')
            axes.plot(tempo, carga_V_BT_SST[Cargas[4]][0][1], label='Com SST (Fases A, B e C)', color="#924C39")
            axes.legend(loc='upper left', fontsize='small', ncol=1, labelspacing=0.15,
                        columnspacing=0.5, handlelength=1, handletextpad=0.3, bbox_to_anchor=(0, 0.36, 0, 0))
            plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # POTÊNCIA Q - 634 ----------------------------------------------------
            fontP = FontProperties()
            fontP.set_size("small")
            fontP.set_family('Times New Roman')
            plt.rcParams["font.family"] = "Times New Roman"
            plt.rcParams.update({'font.size': 18})

            fig, axes = plt.subplots(1, 3, figsize=(11, 4))
            plt.subplots_adjust(wspace=0.2)
            fig.gca().name = "Teste_{:02d}_Carga_634_Q".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes[0].set_xlabel(titulo_eixo.tempo)
            axes[0].set_ylabel(titulo_eixo.carga_Q)
            axes[0].set_ylim([-150, 550])
            axes[0].plot(tempo, carga_Q_TR[Cargas[0]][0], label='Com TR (Fase A)')
            axes[0].plot(tempo, carga_Q_SST[Cargas[0]][0], label='Com SST (Fase A)')

            axes[1].set_xlabel(titulo_eixo.tempo)
            axes[1].set_ylabel(titulo_eixo.carga_Q)
            axes[1].set_ylim([-150, 550])
            axes[1].plot(tempo, carga_Q_TR[Cargas[1]][0], label='Com TR (Fase B)')
            axes[1].plot(tempo, carga_Q_SST[Cargas[1]][0], label='Com SST (Fase B)')

            axes[2].set_xlabel(titulo_eixo.tempo)
            axes[2].set_ylabel(titulo_eixo.carga_Q)
            axes[2].set_ylim([-150, 550])
            axes[2].plot(tempo, carga_Q_TR[Cargas[2]][0], label='Com TR (Fase C)')
            axes[2].plot(tempo, carga_Q_SST[Cargas[2]][0], label='Com SST (Fase C)')

            axes[0].legend(loc='upper left', fontsize='xx-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3) #, bbox_to_anchor=(0, 0.36, 0, 0))
            axes[1].legend(loc='upper left', fontsize='xx-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[2].legend(loc='upper left', fontsize='xx-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            # plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # POTÊNCIA Q - 671  ----------------------------------------------------
            fig, axes = plt.subplots(1, 3, figsize=(11, 4))
            plt.subplots_adjust(wspace=0.2)
            fig.gca().name = "Teste_{:02d}_Carga_671_Q".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes[0].set_xlabel(titulo_eixo.tempo)
            axes[0].set_ylabel(titulo_eixo.carga_Q)
            axes[0].set_ylim([-200, 300])
            axes[0].plot(tempo, carga_Q_TR[Cargas[4]][0], label='Com TR (Fase A)')
            axes[0].plot(tempo, carga_Q_SST[Cargas[4]][0], label='Com SST (Fase A)')

            axes[1].set_xlabel(titulo_eixo.tempo)
            axes[1].set_ylabel(titulo_eixo.carga_Q)
            axes[1].set_ylim([-200, 300])
            axes[1].plot(tempo, carga_Q_TR[Cargas[4]][1], label='Com TR (Fase B)')
            axes[1].plot(tempo, carga_Q_SST[Cargas[4]][1], label='Com SST (Fase B)')

            axes[2].set_xlabel(titulo_eixo.tempo)
            axes[2].set_ylabel(titulo_eixo.carga_Q)
            axes[2].set_ylim([-200, 300])
            axes[2].plot(tempo, carga_Q_TR[Cargas[4]][2], label='Com TR (Fase C)')
            axes[2].plot(tempo, carga_Q_SST[Cargas[4]][2], label='Com SST (Fase C)')

            axes[0].legend(loc='upper left', fontsize='xx-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[1].legend(loc='upper left', fontsize='xx-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[2].legend(loc='upper left', fontsize='xx-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            # plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # POTÊNCIA P - 671  ----------------------------------------------------
            fig, axes = plt.subplots(1, 3, figsize=(11, 4))
            plt.subplots_adjust(wspace=0.2)
            fig.gca().name = "Teste_{:02d}_Carga_671_P".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes[0].set_xlabel(titulo_eixo.tempo)
            axes[0].set_ylabel(titulo_eixo.carga_P)
            axes[0].set_ylim([60, 480])
            axes[0].plot(tempo, carga_P_TR[Cargas[4]][0], label='Com TR (Fase A)')
            axes[0].plot(tempo, carga_P_SST[Cargas[4]][0], label='Com SST (Fase A)')

            axes[1].set_xlabel(titulo_eixo.tempo)
            axes[1].set_ylabel(titulo_eixo.carga_P)
            axes[1].set_ylim([60, 480])
            axes[1].plot(tempo, carga_P_TR[Cargas[4]][1], label='Com TR (Fase B)')
            axes[1].plot(tempo, carga_P_SST[Cargas[4]][1], label='Com SST (Fase B)')

            axes[2].set_xlabel(titulo_eixo.tempo)
            axes[2].set_ylabel(titulo_eixo.carga_P)
            axes[2].set_ylim([60, 480])
            axes[2].plot(tempo, carga_P_TR[Cargas[4]][2], label='Com TR (Fase C)')
            axes[2].plot(tempo, carga_P_SST[Cargas[4]][2], label='Com SST (Fase C)')

            axes[0].legend(loc='upper left', fontsize='x-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[1].legend(loc='upper left', fontsize='x-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[2].legend(loc='upper left', fontsize='x-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            # plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()

            # POTÊNCIA P - 634  ----------------------------------------------------
            fig, axes = plt.subplots(1, 3, figsize=(11, 4))
            plt.subplots_adjust(wspace=0.2)
            fig.gca().name = "Teste_{:02d}_Carga_634_P".format(teste)
            plt.gcf().canvas.set_window_title(fig.gca().name)
            axes[0].set_xlabel(titulo_eixo.tempo)
            axes[0].set_ylabel(titulo_eixo.carga_P)
            axes[0].set_ylim([60, 600])
            axes[0].plot(tempo, carga_P_TR[Cargas[0]][0], label='Com TR (Fase A)')
            axes[0].plot(tempo, carga_P_SST[Cargas[0]][0], label='Com SST (Fase A)')

            axes[1].set_xlabel(titulo_eixo.tempo)
            axes[1].set_ylabel(titulo_eixo.carga_P)
            axes[1].set_ylim([60, 600])
            axes[1].plot(tempo, carga_P_TR[Cargas[1]][0], label='Com TR (Fase B)')
            axes[1].plot(tempo, carga_P_SST[Cargas[1]][0], label='Com SST (Fase B)')

            axes[2].set_xlabel(titulo_eixo.tempo)
            axes[2].set_ylabel(titulo_eixo.carga_P)
            axes[2].set_ylim([60, 600])
            axes[2].plot(tempo, carga_P_TR[Cargas[2]][0], label='Com TR (Fase C)')
            axes[2].plot(tempo, carga_P_SST[Cargas[2]][0], label='Com SST (Fase C)')

            axes[0].legend(loc='upper left', fontsize='x-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[1].legend(loc='upper left', fontsize='x-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            axes[2].legend(loc='upper left', fontsize='x-small', ncol=1, labelspacing=0.15,
                           columnspacing=0.5, handlelength=1, handletextpad=0.3)  # , bbox_to_anchor=(0, 0.36, 0, 0))
            # plot_limites(axes, vminpu, vmaxpu, iteracoes)
            plt.tight_layout()


        figuras = list(map(plt.figure, plt.get_fignums()))
        configuraGraficos(figuras, tempo, iteracoes)

    # obj.Profile(config_pu=config_pu, config_pu_normal=config_pu_normal)

    if msgSimNao("Deseja salvar os gráficos em PDF?", "Salvar figuras"):
        diretorio = diropenbox("Salvar gráficos", "Gráficos", "Plots/")
        if diretorio is not None:
            arquivos = multchoicebox("Escolha os gráficos que deseja salvar", "Escolha", [i.gca().name for i in figuras])
            if arquivos is not None:
                for fig in figuras:
                    if fig.gca().name in arquivos:
                        ExportPDF(fig, diretorio)
                msgBox("Arquivos exportados com sucesso.")
    #
    # obj.Perfil_Tensao()