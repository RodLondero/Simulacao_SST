# -*- coding: utf-8 -*-

import numpy as np
import csv

with open('Fonte_EXP_ElemPowers.csv', newline='') as csvfile:
    # leitura = csv.DictReader(csvfile)
    # P1 = []
    # for linha in leitura:
    #     P1.append(linha[' P_1'].strip())

    leitura = csv.reader(csvfile, delimiter=',', quotechar='"')
    # linhas = sum(1 for row in leitura) - 1

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


    print(potencias)