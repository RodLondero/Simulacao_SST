# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:27:50 2018

@author: Rodolfo Londero
"""
import sys
from easygui import *
from ClassesDSS.Plots import *
from ClassesDSS.DSS import *




obj = DSS("E:/Users/Rodolfo/Documentos/OpenDSS/ProjetoSST/Teste_1/Master_SST.dss")

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
    msgBox("Idioma não definido.",2)
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
tamanho_figuras     = (7, 3.5)

obj.compila_DSS()
obj.CalcVoltageBases([115, 13.8, 0.22*np.sqrt(3)])
# ---------------------------------------------------------------------------------------------------------------------#
# Funções
# ---------------------------------------------------------------------------------------------------------------------#
# Executa comandos no OpenDSS
def comando(text: str):
    dssText.Command(text)

# Define se utiliza SST ou TR
def define_simulacao_com_sst(usa_sst: bool):
    dssCktElement.Enabled("VSource.FonteSST_Carga",     usa_sst)
    dssCktElement.Enabled("Monitor.Potencia_FonteSST",  usa_sst)
    dssCktElement.Enabled("Load.CargaSST_Carga",        usa_sst)
    dssCktElement.Enabled("Transformer.TR",         not usa_sst)

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

def atualiza_SST():
    nome_carga = []
    i = dssLoad.First()
    while i:
        nome = dssLoad.Name()
        if nome.find("cargasst") > -1:
            nome_carga.append(nome.split("_")[1])
        i = dssLoad.Next()

    for nome in nome_carga:
        # Carrega os dados da carga
        dssCktElement.Ativa_Elemento("Load." + nome)
        dssLoad.Name(nome)
        kw = dssLoad.kW()
        kvar = dssLoad.kvar()

        # Atribui ao respectivo SST da carga
        dssCktElement.Ativa_Elemento("Load.CargaSST_" + nome)
        dssLoad.Name("CargaSST_" + nome)
        dssLoad.kW(kw)
        dssLoad.kvar(kvar)
        dssLoad.daily("Unitario_Horas" if passo_simulacao.find('h') > -1 else "Unitario_Minutos")

def adiciona_sst():
    i = dssLoad.First()
    while i:
        nome = dssLoad.Name()
        if dssCktElement.Enabled("Transformer." + nome):
            phases = dssCktElement.NumPhases()
            barra = dssCktElement.get_barras_elemento()[0]
            kv = dssLoad.kV()
            kw = dssLoad.kW()
            conn = "Delta" if dssLoad.IsDelta() else "Wye"
            model = dssLoad.Model()

            # New VSource
            nome_tmp  = " VSource.FonteSST_" + nome
            nome_tmp += " basekv=" + str(kv)
            nome_tmp += " Phases=" + str(phases)
            nome_tmp += " Bus1="   + str(barra) + 'bt'
            comando("New" + nome_tmp)

            # New Load
            nome_tmp  = " Load.CargaSST_" + nome
            nome_tmp += " Bus1="   + str(barra)
            nome_tmp += " Phases=" + str(phases)
            nome_tmp += " Conn="   + conn
            nome_tmp += " kV="     + str(kv)
            nome_tmp += " kW="     + str(kw)
            nome_tmp += " kvar="   + str(0)
            nome_tmp += " Model="  + str(model)
            nome_tmp += " daily="  + "Unitario"

            comando("New" + nome_tmp)

        i = dssLoad.Next()

def getBase(Nome_Elemento: str, terminal: int = 1):
    return dssBus.kVBase(dssCktElement.get_barras_elemento(Nome_Elemento)[terminal]) * 1000

def setSimulacao(teste: int):
    PV, S, FP = False, 200, 0

    if teste == 1:
        PV, FP = False, 1
    elif teste == 2:
        PV, FP = False, 0.9
    elif teste == 3:
        PV, FP = True, 0.9
    else:
        raise Exception('Teste não existe')

    return PV, S, FP
# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# DEFINIÇÃO DOS TESTES
# ---------------------------------------------------------------------------------------------------------------------#
try:
    teste = int(input("Teste: "))
    habilita_PV, SCarga, FPCarga = setSimulacao(teste)
    print("Teste - {}".format(teste))
    print("PV: {}".format("sim" if habilita_PV else "Não"))
    print("Potência da carga: " + str(SCarga) + " kVA")
    print("Fator de Potência da carga: " + str(FPCarga))
except:
    msgBox("Teste não definido", 2)
    sys.exit()
# ---------------------------------------------------------------------------------------------------------------------#
# SIMULAÇÃO APENAS COM TRs
# ---------------------------------------------------------------------------------------------------------------------#
define_simulacao_com_sst(False)
define_LoadsLimitsPU(0.8, 1.1)
define_LoadShapes("Residencial_Minuto" if passo_simulacao.find('m') > -1 else "Residencial")

dssLine.set_linha_by_name("Linha1")
dssLine.tamanho(40)
dssLine.set_linha_by_name("Linha2")
dssLine.tamanho(40)

dssLoad.Name("Carga")
dssLoad.kva(SCarga)
dssLoad.PF(FPCarga)

dssTransformer.Name("TR")
dssTransformer.kva(1, 200)
dssTransformer.kva(2, 200)


carga_V_BT_TR    = zeros(2, iteracoes)
carga_V_MT_TR    = zeros(2, iteracoes)
carga_P_TR       = zeros(iteracoes)
carga_Q_TR       = zeros(iteracoes)
subestacao_P_TR  = zeros(iteracoes)
subestacao_Q_TR  = zeros(iteracoes)
subestacao_FP_TR = zeros(iteracoes)

carga_V_BT_SST    = zeros(2, iteracoes)
carga_V_MT_SST    = zeros(2, iteracoes)
carga_P_SST       = zeros(iteracoes)
carga_Q_SST       = zeros(iteracoes)
subestacao_P_SST  = zeros(iteracoes)
subestacao_Q_SST  = zeros(iteracoes)
subestacao_FP_SST = zeros(iteracoes)
P_vsource_SST     = zeros(iteracoes)

carga_V_BT_TR_sem_pv    = zeros(2, iteracoes)
carga_V_MT_TR_sem_pv    = zeros(2, iteracoes)
carga_P_TR_sem_PV       = zeros(iteracoes)
carga_Q_TR_sem_PV       = zeros(iteracoes)
subestacao_P_TR_sem_PV  = zeros(iteracoes)
subestacao_Q_TR_sem_PV  = zeros(iteracoes)
subestacao_FP_TR_sem_PV = zeros(iteracoes)
# i = 0
# for hora in range_horas:
#     for segundo in range_segundos:
#         dssSolution.Daily(passo        = passo_simulacao,
#                           time_inicial = (hora, segundo),
#                           numero       = 1)
#
#         p_global[0,i], q_global[0, i] = dssCircuit.TotalPower()
#         fp_global[0,i] = calculaFP(p_global[0, i], q_global[0, i])
#
#         p, _ = dssCktElement.Powers("Load.Carga")
#         P_carga_TR[i] = p[0].real
#         Q_carga_TR[i] = p[0].imag
#
#         i += 1

if teste == 3: # Se Teste == 3 - calcula primeiro SEM PV e depois COM PV
    dssCktElement.Enabled("PVSystem.FV", not habilita_PV)
    dssSolution.Daily(passo_simulacao, (hora_inicial, segundo_inicial), iteracoes)

    carga_P_TR_sem_PV       = dssMonitor.getDados("Potencia_Carga", 1)
    carga_Q_TR_sem_PV       = dssMonitor.getDados("Potencia_Carga", 2)
    subestacao_P_TR_sem_PV  = dssMonitor.getDados("Potencia_Subestacao", 1)
    subestacao_Q_TR_sem_PV  = dssMonitor.getDados("Potencia_Subestacao", 2)
    carga_V_BT_TR_sem_pv[0] = dssMonitor.getDados("Tensao_Carga_BT", 1)
    carga_V_BT_TR_sem_pv[1] = dssMonitor.getDados("Tensao_Carga_BT", 1, getBase("Transformer.TR", 1))
    carga_V_MT_TR_sem_pv[0] = dssMonitor.getDados("Tensao_Carga_MT", 1)
    carga_V_MT_TR_sem_pv[1] = dssMonitor.getDados("Tensao_Carga_MT", 1, getBase("Transformer.TR", 0))

dssCktElement.Enabled("PVSystem.FV", habilita_PV)
dssSolution.Daily(passo_simulacao, (hora_inicial, segundo_inicial), iteracoes)

subestacao_P_TR  = dssMonitor.getDados("Potencia_Subestacao", 1)
subestacao_Q_TR  = dssMonitor.getDados("Potencia_Subestacao", 2)
carga_P_TR       = dssMonitor.getDados("Potencia_Carga", 1)
carga_Q_TR       = dssMonitor.getDados("Potencia_Carga", 2)
carga_V_BT_TR[0] = dssMonitor.getDados("Tensao_Carga_BT", 1)
carga_V_BT_TR[1] = dssMonitor.getDados("Tensao_Carga_BT", 1, getBase("Transformer.TR", 1))
carga_V_MT_TR[0] = dssMonitor.getDados("Tensao_Carga_MT", 1)
carga_V_MT_TR[1] = dssMonitor.getDados("Tensao_Carga_MT", 1, getBase("Transformer.TR", 0))


define_simulacao_com_sst(True)
atualiza_SST()

dssTransformer.Name("TR")
kva_base_sst = dssTransformer.kva(1)

comando("Load.CargaSST_Carga.vminpu = 0.8")
comando("Load.CargaSST_Carga.vmaxpu = 1.1")
comando("Load.Carga.vminpu=0.8")
comando("Load.Carga.vmaxpu=1.1")

p_pv = []
p_carga = []

dssLoad.Name("CargaSST_Carga")
dssLoad.kvar(0)

kva_sst_arr=[]
alpha_default = 1

i = 0
for hora in range_horas:
    # print(hora)
    for segundo in range_segundos:
        alpha = alpha_default

        dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

        # Obtém os dados da atuais e atualiza o SST
        p1, _ = dssCktElement.Powers("VSource.FonteSST_Carga")
        P_vsource_SST[i] = -p1[0].real

        dssCktElement.Ativa_Elemento("Load.CargaSST_Carga")
        dssLoad.Name("CargaSST_Carga")
        dssLoad.kW(-p1[0].real * 3)
        dssLoad.kvar(0)

        dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

        v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.CargaSST_Carga")
        v = v1[0] / getBase("Load.CargaSST_Carga", 0)

        p, _ = dssCktElement.TotalPower("VSource.Source")
        fp_tmp = abs(calculaFP(p.real, p.imag))

        if (fp_tmp < fpminpu): #and (fp_tmp > 0.1):
            kvar_1 = 0
            primeiro = 0
            soma = False
            kva_sst = 0
            while (fp_tmp < fpminpu) and (kva_sst < 1):
                q = -p.imag

                if abs(q) < 1:
                    alpha = 0.01

                if (q < 0) and (primeiro == 0):
                    soma = True
                if (q > 0) and (primeiro == 0):
                    soma = False

                # kvar_1 = dssLoad.kvar()
                if soma:
                    kvar_1 += alpha
                else:
                    kvar_1 -= alpha

                primeiro = 1

                # if abs(p.real) < 0.5:
                #     kvar_1 = np.tan(np.arccos(fpminpu)) * p.real

                dssLoad.Name("CargaSST_Carga")

                kw = dssLoad.kW() / kva_base_sst
                kvar = kvar_1 / kva_base_sst

                kva_sst = abs(complex(kw, kvar))
                kva_sst_arr.append(kva_sst)
                if kva_sst < 1:
                    dssLoad.kvar(kvar_1)
                    dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

                    p, q = dssCktElement.TotalPower("VSource.Source")
                    fp_tmp = abs(calculaFP(p.real, p.imag))

            dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

            v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.CargaSST_Carga")
            v = v1[0] / getBase("Load.CargaSST_Carga", 0)

        if v < vminpu:
            kva_sst = 0
            kvar_1 = 0
            while (v < 0.935) and (kva_sst < 1):
                # kvar_1 = dssLoad.kvar()
                kvar_1 -= alpha
                dssLoad.Name("CargaSST_Carga")

                kw = dssLoad.kW() / kva_base_sst
                kvar = kvar_1 / kva_base_sst
                kva_sst = abs(complex(kw, kvar))
                kva_sst_arr.append(kva_sst)

                if kva_sst < 1:
                    dssLoad.kvar(kvar_1)
                    dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

                    v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.CargaSST_Carga")
                    v = v1[0] / getBase("Load.CargaSST_Carga", 0)
            # obj.show_powers_kva_elements()
        elif v > vmaxpu:
            kva_sst = 0
            # kvar_1 = 0
            while (v > vmaxpu) and (kva_sst < 1):
                kvar_1 = dssLoad.kvar()
                kvar_1 += alpha
                dssLoad.Name("CargaSST_Carga")
                kw = dssLoad.kW() / kva_base_sst
                kvar = kvar_1 / kva_base_sst

                kva_sst = abs(complex(kw, kvar))

                if kva_sst < 1:
                    dssLoad.kvar(kvar_1)
                    dssSolution.Daily(passo_simulacao, (hora, segundo), 1)

                    v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.CargaSST_Carga")
                    v = v1[0] / getBase("Load.CargaSST_Carga", 0)
        # else:
        #     dssSolution.Daily(passo         = passo_simulacao,
        #                       time_inicial  = (hora, segundo),
        #                       numero        = 1)

        # Salva as potências da Subestação
        p1, _ = dssCktElement.Powers("VSource.Source")
        subestacao_P_SST[i] = -p1[0].real
        subestacao_Q_SST[i] = -p1[0].imag

        # Salva a potência do SST (MT)
        p1, _ = dssCktElement.Powers("Load.CargaSST_Carga")
        carga_P_SST[i] = p1[0].real
        carga_Q_SST[i] = p1[0].imag

        p1, _ = dssCktElement.Powers("Load.Carga")
        p_carga.append(p1[0].real)
        # Salva a tensão do SST (MT)
        v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.CargaSST_Carga")
        carga_V_MT_SST[0, i] = v1[0]                                      # Valor real
        carga_V_MT_SST[1, i] = v1[0] / getBase("Load.CargaSST_Carga", 0)  # Valor PU

        # Salva a tensão da carga em BT
        v1, _, _, _ = dssCktElement.VoltagesMagAng("Load.Carga")
        carga_V_BT_SST[0, i] = v1[0]                             # Valor real
        carga_V_BT_SST[1, i] = v1[0] / getBase("Load.Carga", 0)  # Valor PU

        p1, _ = dssCktElement.Powers("PVSystem.FV")
        p_pv.append(abs(p1[0].real))

        # if i in [700, 800]:
        #     print(i)
        #     print(P_sub_SST[i])
        #     obj.show_powers_kva_elements()
        #     time.sleep(0.5)
        i += 1

# ----------------------------------------------------------------------------------------------------------------------

figura_subestacao_P, plot_subestacao_P = plt.subplots(1, 1, figsize=tamanho_figuras)
# plt_p_sub.set_title("Substation Active Power")
figura_subestacao_P.gca().name = "Teste_{:02d}_Subestacao_P".format(teste)

plot_subestacao_P.set_xlabel(titulo_eixo.tempo)
plot_subestacao_P.set_ylabel(titulo_eixo.subestacao_P)

if teste == 3:
    plot_subestacao_P.plot(tempo, [-i for i in subestacao_P_TR_sem_PV], label=titulo_eixo.usando_pv, linewidth=1, color="silver")
plot_subestacao_P.plot(tempo, [-i for i in subestacao_P_TR],  label=titulo_eixo.usando_tr,  linewidth=1)
plot_subestacao_P.plot(tempo, [-i for i in subestacao_P_SST], label=titulo_eixo.usando_sst, linewidth=1)

plot_subestacao_P.legend(loc            = 'upper right',
                         fontsize       = 'small',
                         ncol           = 3,
                         columnspacing  = 0.5,
                         handlelength   = 1,
                         handletextpad  = 0.3,
                         labelspacing   = 0)
plt.tight_layout()
plt.gcf().canvas.set_window_title(figura_subestacao_P.gca().name)
# ----------------------------------------------------------------------------------------------------------------------
figura_subestacao_Q, plot_subestacao_Q = plt.subplots(1, 1, figsize=tamanho_figuras)
# plt_q_sub.set_title("Substation Reactive Power")
figura_subestacao_Q.gca().name = "Teste_{:02d}_Subestacao_Q".format(teste)
plot_subestacao_Q.set_xlabel(titulo_eixo.tempo)
plot_subestacao_Q.set_ylabel(titulo_eixo.subestacao_Q)
if teste == 3:
    plot_subestacao_Q.plot(tempo, [-i for i in subestacao_Q_TR_sem_PV], label=titulo_eixo.usando_pv, linewidth=1, color="red")
plot_subestacao_Q.plot(tempo, [-i for i in subestacao_Q_TR],  label=titulo_eixo.usando_tr,  linewidth=1)
plot_subestacao_Q.plot(tempo, [-i for i in subestacao_Q_SST], label=titulo_eixo.usando_sst, linewidth=1)
plot_subestacao_Q.legend(loc            = 'best',
                         fontsize       = 'small',
                         ncol           = 3,
                         columnspacing  = 0.5,
                         handlelength   = 1,
                         handletextpad  = 0.3,
                         labelspacing   = 0)
plt.tight_layout()
plt.gcf().canvas.set_window_title(figura_subestacao_Q.gca().name)
# ----------------------------------------------------------------------------------------------------------------------
figura_carga_P, plot_carga_P = plt.subplots(1, 1, figsize=tamanho_figuras)
# plt_p_carga.set_title("Load Active Power")
figura_carga_P.gca().name = "Teste_{:02d}_Carga_P".format(teste)
plot_carga_P.set_xlabel(titulo_eixo.tempo)
plot_carga_P.set_ylabel(titulo_eixo.carga_P)
if teste == 3:
    plot_carga_P.plot(tempo, carga_P_TR_sem_PV, label=titulo_eixo.usando_pv, linewidth=1, color="silver")
plot_carga_P.plot(tempo, carga_P_TR,  label=titulo_eixo.usando_tr, linewidth=1)
plot_carga_P.plot(tempo, carga_P_SST, label=titulo_eixo.usando_sst, linewidth=1)
plot_carga_P.legend(loc            = 'upper left',
                    fontsize       = 'small',
                    ncol           = 3,
                    columnspacing  = 0.5,
                    handlelength   = 1,
                    handletextpad  = 0.3,
                    labelspacing   = 0)
plt.tight_layout()
plt.gcf().canvas.set_window_title(figura_carga_P.gca().name)
# ----------------------------------------------------------------------------------------------------------------------
figura_carga_V_BT, plot_carga_V_BT = plt.subplots(1, 1, figsize=tamanho_figuras)
#lt_v_carga_bt.set_title("Load Voltage LV")
figura_carga_V_BT.gca().name = "Teste_{:02d}_Carga_V_BT".format(teste)
plot_carga_V_BT.set_xlabel(titulo_eixo.tempo)
plot_carga_V_BT.set_ylabel(titulo_eixo.carga_V)
if teste == 3:
    plot_carga_V_BT.plot(tempo, carga_V_BT_TR_sem_pv[1], label=titulo_eixo.usando_pv, linewidth=1, color="silver")
plot_carga_V_BT.plot(tempo, carga_V_BT_TR[1],        label=titulo_eixo.usando_tr,   linewidth=1)
plot_carga_V_BT.plot(tempo, carga_V_BT_SST[1],       label=titulo_eixo.usando_sst,  linewidth=1)
plot_carga_V_BT.legend(loc              = 'upper right',
                       bbox_to_anchor   = (1, 0.96),
                       fontsize         = 'small',
                       ncol             = 3,
                       columnspacing    = 0.5,
                       handlelength     = 1,
                       handletextpad    = 0.3,
                       labelspacing     = 0)
plot_limites(plot_carga_V_BT, vminpu, vmaxpu, iteracoes)
plt.tight_layout()
plt.gcf().canvas.set_window_title(figura_carga_V_BT.gca().name)
# ----------------------------------------------------------------------------------------------------------------------
figura_carga_V_MT, plot_carga_V_MT = plt.subplots(1, 1, figsize=tamanho_figuras)
#plt_v_carga_mt.set_title("Load Voltage MV")
figura_carga_V_MT.gca().name = "Teste_{:02d}_Carga_V_MT".format(teste)
plot_carga_V_MT.set_xlabel(titulo_eixo.tempo)
plot_carga_V_MT.set_ylabel(titulo_eixo.carga_V)
if teste == 3:
    plot_carga_V_MT.plot(tempo, carga_V_MT_TR_sem_pv[1], label=titulo_eixo.usando_pv, linewidth=1, color="silver")
plot_carga_V_MT.plot(tempo, carga_V_MT_TR[1],  label=titulo_eixo.usando_tr,  linewidth=1)
plot_carga_V_MT.plot(tempo, carga_V_MT_SST[1], label=titulo_eixo.usando_sst, linewidth=1)
plot_carga_V_MT.legend(loc              = 'upper right',
                       bbox_to_anchor   = (1, 0.96),
                       fontsize         = 'small',
                       ncol             = 3,
                       columnspacing    = 0.5,
                       handlelength     = 1,
                       handletextpad    = 0.3,
                       labelspacing     = 0)
plot_limites(plot_carga_V_MT, vminpu, vmaxpu, iteracoes)
plt.tight_layout()
plt.gcf().canvas.set_window_title(figura_carga_V_MT.gca().name)
# ----------------------------------------------------------------------------------------------------------------------
figura_loadshape, plot_loadshape = plt.subplots(1, 1, figsize=tamanho_figuras)
#plt_v_carga_mt.set_title("Load Voltage MV")
figura_loadshape.gca().name = "Teste_{:02d}_Loadshape".format(teste)
plot_loadshape.set_xlabel(titulo_eixo.tempo)
plot_loadshape.set_ylabel("Multiplier")
obj.dssLoadShapes.Name("Residencial_Minuto")
plot_loadshape.plot(tempo, obj.dssLoadShapes.Pmult(), linewidth=1)
plt.tight_layout()
# ----------------------------------------------------------------------------------------------------------------------

for i in range(0, len(subestacao_P_TR)):
    if teste == 3:
        subestacao_FP_TR_sem_PV[i] = calculaFP(subestacao_P_TR_sem_PV[i], subestacao_Q_TR_sem_PV[i])
    subestacao_FP_TR[i]  = calculaFP(subestacao_P_TR[i],  subestacao_Q_TR[i])
    subestacao_FP_SST[i] = calculaFP(subestacao_P_SST[i], subestacao_Q_SST[i])

if teste == 3:
    tamanho_figuras = (7, 4)
figura_subestacao_FP, plot_subestacao_FP = plt.subplots(1, 1, figsize=tamanho_figuras)
figura_subestacao_FP.gca().name = "Teste_{:02d}_Subestacao_FP".format(teste)

plot_subestacao_FP.set_xlabel(titulo_eixo.tempo)
plot_subestacao_FP.set_ylabel(titulo_eixo.subestacao_FP)

if teste == 3:
    plot_subestacao_FP.plot(tempo, subestacao_FP_TR_sem_PV, label=titulo_eixo.usando_pv, linewidth=1, color="silver")
plot_subestacao_FP.plot(tempo, subestacao_FP_TR, label=titulo_eixo.usando_tr, linewidth=1)
plot_subestacao_FP.plot(tempo, subestacao_FP_SST, label=titulo_eixo.usando_sst, linewidth=1)
plot_subestacao_FP.legend(loc            = 'lower right',
                          bbox_to_anchor = (1, 0),
                          fontsize       = 'small',
                          ncol           = 3,
                          columnspacing  = 0.5,
                          handlelength   = 1,
                          handletextpad  = 0.3,
                          labelspacing   = 0)
plot_subestacao_FP.set_ylim([fpminpu-0.02, fpmaxpu+0.02])
plot_limites(plot_subestacao_FP, fpminpu, fpmaxpu, iteracoes)
plt.tight_layout()
plt.gcf().canvas.set_window_title(figura_subestacao_FP.gca().name)

figuras = list(map(plt.figure, plt.get_fignums()))
configuraGraficos(figuras, tempo, iteracoes)

plt.pause(0.1)
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

if msgSimNao("Deseja salvar os gráficos em PDF?", "Salvar figuras"):
    diretorio = diropenbox("Salvar gráficos", "Gráficos", "Plots/")
    if diretorio is not None:
        arquivos = multchoicebox("Escolha os gráficos que deseja salvar", "Escolha", [i.gca().name for i in figuras])
        if arquivos is not None:
            for fig in figuras:
                if fig.gca().name in arquivos:
                    ExportPDF(fig, diretorio)
            msgBox("Arquivos exportados com sucesso.")
# # ----------------------------------------------------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------------------------------------------------#
# GERA RESULTADOS EM CSV
# ---------------------------------------------------------------------------------------------------------------------#
if msgSimNao("Deseja salvar o arquivo .CSV com os resultados?", "Salvar Resultados"):
    arquivo = filesavebox("Salvar arquivo de resultados?", filetypes=["*.csv"], default="Resultados/Resultado_Teste_{}.csv".format(teste))
    if arquivo is not None:
        try:
            with open(arquivo, mode='w', newline='') as potencia_sub:
                writer = csv.writer(potencia_sub, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['Hora',
                                 'Psub(TR)',
                                 'Qsub(TR)',
                                 'FP(TR)',
                                 'Psub(SST)',
                                 'Qsub(SST)',
                                 'FP(SST)',
                                 'P (SST)',
                                 'Q (SST)',
                                 'S (SST)'
                                 ])
                for i in range(iteracoes):
                    writer.writerow([i+1,
                                     round(subestacao_P_TR[i], 4),
                                     round(subestacao_Q_TR[i], 4),
                                     round(calculaFP(subestacao_P_TR[i], subestacao_Q_TR[i]), 4),
                                     round(subestacao_P_SST[i], 4),
                                     round(subestacao_Q_SST[i], 4),
                                     round(calculaFP(subestacao_P_TR[i], subestacao_Q_SST[i]), 4),
                                     round(carga_P_SST[i], 4),
                                     round(carga_Q_SST[i], 4),
                                     round(np.sqrt(np.square(carga_Q_SST[i]) + np.square(carga_P_SST[i])))
                                      ])
            msgBox("Arquivo gerado com sucesso.", 0)
        except:
            msgBox("Não foi possível gerar o arquivo.", 2)
