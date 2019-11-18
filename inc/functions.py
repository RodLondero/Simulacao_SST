# -*- coding: utf-8 -*-
import numpy as np

def setRede(rede: int):
    redes = {0: 'RedeBasica',
             1: 'Rede13Barras'}    
    return redes[rede]

def zeros(linhas, colunas = None):
    """ Cria uma matriz/vetor de zero

    :param linhas: número de linhas da matriz
    :param colunas: número de colunas da matriz
    """
    if linhas is not None and colunas is None:
        return np.zeros(linhas)
    else:
        return np.zeros([linhas, colunas])
    
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
            angulo = np.arctan(q[i]/p[i])
            fp.append(np.cos(angulo))
    return fp 

