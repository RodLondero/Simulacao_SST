# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:37:00 2019

@author: Rodolfo
"""
import os
import pathlib

import py_dss_interface


class SST(object):

    def __init__(self, dss: py_dss_interface.DSSDLL, name: str, buses: list[str], num_phases: int, voltages_ll: list,
                 kW: float, kvar: float, load_shape: str = ''):
        self.name = name
        self.vsource_name = "VSource." + name
        self.load_name = "Load." + name
        self.num_phases = num_phases
        self.conn = 'wye'
        self.model = 1
        self.kW = kW
        self.kvar = kvar
        self.load_shape = load_shape

        self.bus1 = buses[0]
        self.vl_1 = voltages_ll[0]

        self.bus2 = buses[1]
        self.vl_2 = voltages_ll[1]

        self.dss = dss

        self.create_vsource()
        self.create_load()
        self.create_voltage_monitors()
        self.create_power_monitors()

    def __str__(self):
        return 'teste'

    def __execCommand(self, comando):
        self.dss.text(comando)

    def create_vsource(self):
        cmd = f"New VSource.{self.name} Bus1={self.bus1} Phases={self.num_phases} basekV={self.vl_1}"
        self.__execCommand(cmd)

    def create_load(self):
        cmd = f"New Load.{self.name} Bus1={self.bus2} Phases={self.num_phases} Conn={self.conn} Model={self.model} " \
              f"                      kV={self.vl_2}     kw={self.kW}          kvar={self.kvar}    daily={self.load_shape}"
        self.__execCommand(cmd)

    def create_voltage_monitors(self):
        # Código DSS para criação do monitor de tensão da FONTE do SST

        cmd_v_fonte = f"New Monitor.Tensao_Fonte_{self.name}  element = VSource.{self.name} " \
                      f"                                     terminal = 1" \
                      f"                                         mode = 0 " \
                      f"                                       ppolar = no"

        cmd_v_carga = f"New Monitor.Tensao_Carga_{self.name}  element = Load.{self.name} " \
                      f"                                     terminal = 1" \
                      f"                                         mode = 0 " \
                      f"                                       ppolar = no"

        self.__execCommand(cmd_v_fonte)
        self.__execCommand(cmd_v_carga)

    def create_power_monitors(self):
        # Código DSS para criação do monitor de POTÊNCIA da FONTE do SST

        cmd_p_fonte = f"New Monitor.Potencia_Fonte_{self.name}  element = VSource.{self.name} " \
                      f"                                       terminal = 1" \
                      f"                                           mode = 1 " \
                      f"                                         ppolar = no"

        cmd_p_carga = f"New Monitor.Potencia_Carga_{self.name}  element = Load.{self.name} " \
                      f"                                       terminal = 1" \
                      f"                                           mode = 1 " \
                      f"                                         ppolar = no"

        # Executa os comandos no OpenDSS
        self.__execCommand(cmd_p_fonte)
        self.__execCommand(cmd_p_carga)

    def Enabled(self, enabled: bool):
        self.dss.circuit_set_active_element(self.load_name)
        self.dss.cktelement_write_enabled(int(enabled))

        self.dss.circuit_set_active_element(self.vsource_name)
        self.dss.cktelement_write_enabled(int(enabled))

    @staticmethod
    def getAllSST(dss: py_dss_interface.DSSDLL):
        name = []
        names = []

        for element in dss.circuit_all_element_names():
            if element.find('sst') != -1:
                name.append(element)
                if len(name) == 6:
                    names.append(name)
                    name = []

        return names[0] if len(names) == 1 else names

    @staticmethod
    def getPowerSST(self):
        try:
            # Terminal 1 -> VSource
            # Terminal 2 -> Load

            self.dss.circuit_set_active_element(self.vsource_name)  # Ativa o elemento
            powers_primary = self.dss.cktelement_powers()[:2]  # Obtém as potências

            self.dss.circuit_set_active_element(self.load_name)  # Ativa o elemento
            powers_secondary = self.dss.cktelement_powers()[:2]  # Obtém as potências

            return powers_primary + powers_secondary

        except Exception as e:
            msg = "Erro na funçao getPowerSST(): "
            if e.__class__ is AttributeError:
                msg += "Elemento informado não é um SST!"
            else:
                msg += str(e.__class__) + " -> " + str(e)

            return msg


if __name__ == '__main__':
    # Get the root folder
    script_path = os.path.dirname(os.path.abspath(__file__))

    # Get Master.dss paths
    dss_file_rede_basica = pathlib.Path(script_path).joinpath("RedeBasica", "Master.dss")
    dss_file_rede_13bus = pathlib.Path(script_path).joinpath("Rede13Barras", "Master.dss")

    # Initialize py-dss-interface
    dss = py_dss_interface.DSSDLL()

    dss.text(f"Compile [{dss_file_rede_basica}]")

    dss.text("Set Voltagebases=[115, 13.8, .38]")
    dss.text("calcvoltagebases")

    dss.solution_solve()

    s = SST(dss,
            name="SST1",
            buses=['barra2', 'barra3'],
            num_phases=1,
            voltages_ll=[13.8, 0.22],
            kW=100,
            kvar=10)

    dss.solution_solve()

    print(SST.getPowerSST(s))

    dss.text("show Isolated")
    dss.text("Show Voltage LN Elements")
