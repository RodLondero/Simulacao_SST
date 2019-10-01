# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 21:03:51 2019

@author: Rodolfo
"""
import dss, os, sys
import tkinter
from tkinter import messagebox

class mDSS(object):
    def __init__(self, dssFileName: str):
        """
        :param dssFileName: Caminho completo do arquivo .dss
        """

        self.dssFileName = dssFileName.replace('"', '')

        # Criar a conexão entre Python e OpenDSS
        dss.use_com_compat()
        self.dssObj = dss.DSS
        
        try:
            # Iniciar o Objeto DSS
            if not self.dssObj.Start(0):
                raise Exception("Problemas em iniciar o OpenDSS")
            else:
                # Criar variáveis para as principais interfaces
                try:
                    self.dssText            = self.dssObj.Text
                    self.dssCircuit         = self.dssObj.ActiveCircuit
                    self.dssCktElement      = self.dssCircuit.ActiveCktElement
                    self.dssBus             = self.dssCircuit.ActiveBus
                    self.dssLines           = self.dssCircuit.Lines
                    self.dssLoads           = self.dssCircuit.Loads
                    self.dssTransformers    = self.dssCircuit.Transformers
                    self.dssMonitors        = self.dssCircuit.Monitors
                    self.dssSolution        = self.dssCircuit.Solution
                    self.dssLineCodes       = self.dssCircuit.LineCodes
                    self.dssLoadShapes      = self.dssCircuit.LoadShapes
                
                    self.dir_principal      = self.dssFileName.rstrip(self.dssFileName.split('/')[len(self.dssFileName.split('/'))-1])
                    self.dir_resultados     = self.dir_principal + "Resultados"
                    self.dir_plots          = self.dir_principal + "Plots"
                    
                    self.dssObj.DataPath    = self.dir_principal
                    os.chdir("..")
                except:
                    raise Exception("Erro ao criar interfaces!")
                    
        except Exception as e:              
            print(e)
            root = tkinter.Tk()
            root.withdraw()
            root.focus_displayof()
            messagebox.showerror('Erro',e)            
            sys.exit()
            
    def versao_DSS(self):
        return self.dssObj.Version

    def compila_DSS(self):
        # Limpar informações da última simulação
        self.dssObj.ClearAll()
        self.dssText.Command = "Compile \"" + self.dssFileName + "\""
        os.chdir("..")
        return self.dssText.Result
    
        