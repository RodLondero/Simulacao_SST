# -*- coding: utf-8 -*-
from matplotlib.ticker import (AutoMinorLocator)
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as ticker


dir_plots = os.getcwd() + '/Plots/'

# ----------------------------------------------------------------------------------------------------------------------
def ExportPDF(plot, local: str):
    plot.savefig(local + "\\" + plot.gca().name + ".pdf", bbox_inches="tight", pad_inches=0)
# ----------------------------------------------------------------------------------------------------------------------
def plot_limites(ax, min, max, t):
    """ Plota os limites de desejados

    :param ax:  plot
    :param min: Limite inferior
    :param max: Limite superior
    """

    ax.plot([1, t], [min, min], 'r')
    ax.plot([1, t], [max, max], 'r')
# ----------------------------------------------------------------------------------------------------------------------
def configuraGraficos(figs, tempo, t):
    for fig in figs:
        for ax in fig.axes:
            ax.set_xlim([0, t])
            x = tempo
            if len(tempo) > 24:
                ax.set_xlim([60, t])
                x = np.arange(60, t + 60, 60)
            ax.set_xticks(x)
            ax.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax.yaxis.set_minor_locator(AutoMinorLocator(5))
            ax.grid(True)
            ax.grid(b=True, which='minor', color='#DCDCDC')

            if len(tempo) > 24:
                fig.canvas.draw()
                labels = [item.get_text() for item in ax.get_xticklabels()]
                for i in range(0, len(labels)):
                    # if i == 0:
                    #     labels[i] = str(int(int(labels[i]) / 60))
                    # elif i >= 0 and (i+1) % 4 == 0:
                    if i >= 0:
                        labels[i] = str(int(int(labels[i]) / 60))
                    else:
                        labels[i] = ""
                ax.set_xticklabels(labels)
                # ----------------------------------------------------------------------------------------------------------------------
def plot_subestacao_P_ativa(P_antes, P_depois):
    fig3, ax = plt.subplots()
    ax.set_title("Subestação")
    ax.plot(range(1, 25), P_antes)
    ax.plot(range(1, 25), P_depois)
    ax.set_xlabel("Tempo (h)")
    ax.set_ylabel("Potência (kW)")
    ax.set_xticks(range(1, 25))
    ax.set_xlim([1, 24])
    ax.legend(["Sem PV", "Com PV"])
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True)
    ax.grid(b=True, which='minor', color='#DCDCDC')
# ----------------------------------------------------------------------------------------------------------------------
def plot_sst_P_reativa(Q):
    fig3, ax = plt.subplots()
    ax.plot(range(1, 25), np.array(Q), color="green")
    ax.set_xlabel("Tempo (h)")
    ax.set_ylabel("Potência (kvar)")
    ax.set_xticks(np.arange(1, 25))
    ax.set_xlim([1, 24])
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True)
    ax.grid(b=True, which='minor', color='#DCDCDC')
# ----------------------------------------------------------------------------------------------------------------------
def plot_subestacao_fp(P, Q, Pnovo=None, Qnovo=None):
    fig5, ax = plt.subplots()

    fp = np.cos(np.arctan(np.array(Q) / np.array(P)))
    ax.plot(range(1, 25), fp, label="FP anterior")

    if (Pnovo is not None) and (Qnovo is not None):
        fp_novo = np.cos(np.arctan(np.array(Qnovo) / np.array(Pnovo)))
        ax.plot(range(1, 25), fp_novo, label="FP Novo")

    ax.set_xlabel("Tempo (h)")
    ax.set_ylabel("Fator de Potência")
    ax.set_xticks(np.arange(1, 25))
    ax.set_xlim([1, 24])
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.legend()
    ax.grid(True)
    ax.grid(b=True, which='minor', color='#DCDCDC')
# ----------------------------------------------------------------------------------------------------------------------

