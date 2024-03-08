# -*- coding: utf-8 -*-

import numpy as np
import csv
import tkinter
from tkinter import messagebox
from tkinter import ttk
import time


# ----------------------------------------------------------------------------------------------------------------------
def zeros(linhas, colunas = None):
    """ Cria uma matriz/vetor de zero

    :param linhas: número de linhas da matriz
    :param colunas: número de colunas da matriz
    """
    if linhas is not None and colunas is None:
        return np.zeros(linhas)
    else:
        return np.zeros([linhas, colunas])
# ----------------------------------------------------------------------------------------------------------------------
def calculaFP(p, q):
    """ Realiza o cálculo do Fator de Potência

    :param p: Potência Ativa (número ou lista)
    :param q: Potência Reativa (número ou lista)
    """
    if type(p) in [int, float, np.float64]:
        # s = abs(np.complex(p, q))
        # fp = abs(p) / s
        angulo = np.arctan(q/p)
        fp = np.cos(angulo)
    else:
        fp = []
        for i in range(0, len(p)):
            # s = np.complex(p[i], q[i])
            angulo = np.arctan(q/p)
            fp.append(np.cos(angulo))
    return fp
# ----------------------------------------------------------------------------------------------------------------------
def lerArquivoPotencias():
    with open('Fonte_EXP_ElemPowers.csv', newline='') as csvfile:

        leitura = csv.reader(csvfile, delimiter=',', quotechar='"')

        P1, P2, nomeElemento, contador = [], [], [], 0

        linha = iter(leitura)
        # linha.__init__()
        next(linha)
        for linha in leitura:
            numCondutores = float(linha[2].strip())
            numTerminais = float(linha[1].strip())
            nomeElemento.append(linha[0].strip())

            P1_tmp = np.zeros(4, dtype=complex)
            P2_tmp = np.zeros(4, dtype=complex)

            if numCondutores == 4:
                idx = 0
                for i in range(3, 11, 2):
                    p_tmp = float(linha[i].strip())
                    q_tmp = float(linha[i + 1].strip())

                    if p_tmp == 0 and q_tmp == 0:
                        pass
                    else:
                        P1_tmp[idx] = np.complex(p_tmp, q_tmp)

                    idx += 1

                if numTerminais == 2:
                    idx = 0
                    for i in range(11, 19, 2):
                        p_tmp = float(linha[i].strip())
                        q_tmp = float(linha[i + 1].strip())

                        if p_tmp == 0 and q_tmp == 0:
                            pass
                        else:
                            P2_tmp[idx] = np.complex(p_tmp, q_tmp)

                        idx += 1

            elif numCondutores == 3:
                idx = 0
                for i in range(3, 9, 2):
                    p_tmp = float(linha[i].strip())
                    q_tmp = float(linha[i + 1].strip())

                    if p_tmp == 0 and q_tmp == 0:
                        pass
                    else:
                        P1_tmp[idx] = np.complex(p_tmp, q_tmp)

                    idx += 1

                if numTerminais == 2:
                    idx = 0
                    for i in range(9, 15, 2):
                        p_tmp = float(linha[i].strip())
                        q_tmp = float(linha[i + 1].strip())

                        if p_tmp == 0 and q_tmp == 0:
                            pass
                        else:
                            P2_tmp[idx] = np.complex(p_tmp, q_tmp)

                        idx += 1

            if contador == 0:
                P1 = [list(P1_tmp)]
                P2 = [list(P2_tmp)]
            else:
                P1.append(list(P1_tmp))
                P2.append(list(P2_tmp))

            contador += 1

        potencias = {}
        for i in range(0, len(nomeElemento), 1):
            potencias[nomeElemento[i]] = {'P1': P1[i], 'P2': P2[i]}

        return potencias, nomeElemento, P1, P2
#---------------------------------------------------------------------------------------------------------------------
def sleep(sec: float):
    time.sleep(sec)

def msgBox(mensagem: str, tipo: int = 0):
    root = tkinter.Tk()
    root.withdraw()
    if tipo == 0:
        messagebox.showinfo("Informação", mensagem)
    elif tipo == 1:
        messagebox.showwarning("Aviso", mensagem)
    elif tipo == 2:
        messagebox.showerror("Erro", mensagem)
    else:
        raise Exception("Opção inválida")

def msgSimNao(titulo: str, mensagem: str):
    root = tkinter.Tk()
    root.withdraw()
    return messagebox.askyesno(titulo, mensagem)


class titulo_eixo(object):
    def __init__(self, idioma):
        if idioma == "pt":
            self.carga_P         = "Potêncica Ativa (kW)"
            self.carga_V         = "Tensão (p.u)"
            self.subestacao_P    = "Potência Ativa (kW)"
            self.subestacao_Q    = "Potência Reativa (kvar)"
            self.subestacao_FP   = "Fator de Potência"
            self.tempo           = "Tempo (h)"
            self.usando_tr       = "Com TR"
            self.usando_sst      = "Com SST"
            self.usando_pv       = "Sem FV"
        elif idioma == "en":
            self.carga_P         = "Active Power (kW)"
            self.carga_V         = "Voltage (p.u)"
            self.subestacao_P    = "Active Power (kW)"
            self.subestacao_Q    = "Reactive Power (kvar)"
            self.subestacao_FP   = "Power Factor"
            self.tempo           = "Time (h)"
            self.usando_tr       = "Using LFT"
            self.usando_sst      = "Using SST"
            self.usando_pv       = "Without PV"
        else:
            raise Exception("Idioma não definido.")