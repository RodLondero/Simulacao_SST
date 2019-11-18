# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:37:00 2019

@author: Rodolfo
"""
from mDSS import mDSS
import traceback

class SST(object):
    
    def __init__(self, dssObj: mDSS, Name: str, Buses: list, NumPhases: int, VL: list, S: complex, LoadShape: str = ''):
        self.Name        = Name
        self.VSourceName = "VSource." + Name
        self.LoadName    = "Load."    + Name
        self.NumPhases   = NumPhases
        self.Conn        = 'wye'
        self.Model       = 1
        self.P           = S.real
        self.Q           = S.imag
        self.LoadShape   = LoadShape
        
        self.Bus1 = Buses[0]
        self.VL_1 = VL[0]
        
        self.Bus2 = Buses[1]        
        self.VL_2 = VL[1]
        
        self.dssObj        = dssObj
        self.dssCircuit    = dssObj.dssCircuit
        self.dssCktElement = dssObj.dssCktElement
        
        #print(dssObj.dssLoads.AllNames)
        #print(str( self.dssObj.dssCircuit.AllElementNames))
        #print(str( self.dssObj.dssCircuit.AllBusNames))
        self.CreateVSource()
        self.CreateLoad()
        self.CreateVoltageMonitors()
        self.CreatePowerMonitors()
        #print()
        #print(str( self.dssObj.dssCircuit.AllElementNames))
        #print(str( self.dssObj.dssCircuit.AllBusNames))
            
    def __str__(self):
        return 'teste'
    
    def __execCommand(self, comando):
        self.dssObj.dssText.Command = comando
    
    def CreateVSource(self):
        cmd =  ' New VSource.'  + self.Name
        cmd += '     Bus1   = ' + str(self.Bus1)
        cmd += '     Phases = ' + str(self.NumPhases)
        cmd += '     basekV = ' + str(self.VL_1)
        
        self.__execCommand(cmd)
    
    def CreateLoad(self):
        cmd  = 'New Load.'      + self.Name
        cmd += '     Bus1   = ' + str(self.Bus2)
        cmd += '     Phases = ' + str(self.NumPhases)
        cmd += '     Conn   = ' + str(self.Conn)
        cmd += '     Model  = ' + str(self.Model)
        cmd += '     kV     = ' + str(self.VL_2)
        cmd += '     kw     = ' + str(self.P)
        cmd += '     kvar   = ' + str(self.Q)
        cmd += '     daily  = ' + str(self.LoadShape)
        
        self.__execCommand(cmd)
    
    def CreateVoltageMonitors(self):
        # Código DSS para criação do monitor de tensão da FONTE do SST
        cmd_v_fonte  = ' New Monitor.Tensao_Fonte_{name}'.format(name=self.Name)
        cmd_v_fonte  = ' '.join([cmd_v_fonte,' element  = VSource.{name}'.format(name=self.Name)])
        cmd_v_fonte  = ' '.join([cmd_v_fonte,' terminal = 1'])
        cmd_v_fonte  = ' '.join([cmd_v_fonte,' mode     = 0'])
        cmd_v_fonte  = ' '.join([cmd_v_fonte,' ppolar   = no'])
           
        # Código DSS para criação do monitor de tensão da CARGA do SST
        cmd_v_carga  = ' New Monitor.Tensao_Carga_{name}'.format(name=self.Name)
        cmd_v_carga  = ' '.join([cmd_v_carga,' element  = Load.{name}'.format(name=self.Name)])
        cmd_v_carga  = ' '.join([cmd_v_carga,' terminal = 1'])
        cmd_v_carga  = ' '.join([cmd_v_carga,' mode     = 0'])
        cmd_v_carga  = ' '.join([cmd_v_carga,' ppolar   = no'])
        
        # Executa os comandos no OpenDSS
        self.__execCommand(cmd_v_fonte)
        self.__execCommand(cmd_v_carga)
    
    def CreatePowerMonitors(self):
        # Código DSS para criação do monitor de POTÊNCIA da FONTE do SST
        cmd_p_fonte  = ' New Monitor.Potencia_Fonte_{name}'.format(name=self.Name)
        cmd_p_fonte  = ' '.join([cmd_p_fonte,' element  = VSource.{name}'.format(name=self.Name)])
        cmd_p_fonte  = ' '.join([cmd_p_fonte,' terminal = 1'])
        cmd_p_fonte  = ' '.join([cmd_p_fonte,' mode     = 1'])
        cmd_p_fonte  = ' '.join([cmd_p_fonte,' ppolar   = no'])
        
        # Código DSS para criação do monitor de POTÊNCIA da CARGA do SST
        cmd_p_carga  = ' New Monitor.Potencia_Carga_{name}'.format(name=self.Name)
        cmd_p_carga  = ' '.join([cmd_p_carga,' element  = Load.{name}'.format(name=self.Name)])
        cmd_p_carga  = ' '.join([cmd_p_carga,' terminal = 1'])
        cmd_p_carga  = ' '.join([cmd_p_carga,' mode     = 1'])
        cmd_p_carga  = ' '.join([cmd_p_carga,' ppolar   = no'])
        
        # Executa os comandos no OpenDSS
        self.__execCommand(cmd_p_fonte)
        self.__execCommand(cmd_p_carga)
    
    def Enabled(self, enabled: bool):
        self.dssCircuit.SetActiveElement(self.LoadName)
        self.dssCktElement.Enabled = enabled
        self.dssCircuit.SetActiveElement(self.VSourceName)
        self.dssCktElement.Enabled = enabled
        
    def getAllSST(self):
        name  = []
        names = []        

        for element in self.dssObj.dssCircuit.AllElementNames:   
            if element.find('sst') != -1:
                name.append(element)    
                if len(name) == 6:
                    names.append(name)
                    name = []
                    
        return names
    
    @staticmethod
    def getPowerSST(self, terminal: int):
        try:       
            # Obtém o nome do elemento SST com base no terminal
            # Terminal 1 -> VSource
            # Terminal 2 -> Load
            nome = {1:self.VSourceName, 2: self.LoadName}[terminal]
            
            self.dssCircuit.SetActiveElement(nome)  # Ativa o elemento
            Powers = self.dssCktElement.Powers      # Obtém as potências
            
            s = []
    
            # Loop para organizar as potências em P+jQ
            # se 'par'   é P
            # se 'ímpar' é Q
            for i in range(0, len(Powers)):         
                if i % 2 == 0:
                    p = Powers[i]
                else:
                    q = Powers[i]
                    s.append(complex(p, q))
                    p = 0
                    q = 0
                
            return s
        except Exception as e:
            msg = "Erro na funçao getPowerSST(): "
            if e.__class__ is AttributeError:
                msg += "Elemento informado não é um SST!"
            elif e.__class__ is KeyError:
                msg += "Terminal não existe!"
            else:
                msg += str(e.__class__) + " -> " + str(e)
                          
            return msg
    
if __name__ == '__main__':
    
    from mDSS import mDSS
    import os
    import inc.functions as f
    
    dssObj = mDSS(os.getcwd() + "\\" + f.setRede(0) + "\\Master.dss")
    
    print(dssObj.compila_DSS())
    
    dssObj.dssText.Command = "Set Voltagebases=[115, 13.8, .38]"
    dssObj.dssText.Command = "calcvoltagebases"
    
    dssObj.dssSolution.Solve()
    
    
    s = SST(dssObj, 
            'SST1', 
            ['barra2', 'barra3'], 
            1, 
            [13.8, 0.22], 
            100+10j)
    
#    s1 = SST(dssObj, 
#            'SST2', 
#            ['barra2', 'barra3'], 
#            1, 
#            [13.8, 0.22], 
#            100+10j)
    
    dssObj.dssSolution.Solve()
    #print(s1.getAllSST())
    
    print(SST.getPowerSST(s, 1))
    print(SST.getPowerSST(s, 2))
    
#    dssObj.showIsolated()
#    dssObj.showPowerskVAElements()
#    dssObj.showVoltagesLNElements()
