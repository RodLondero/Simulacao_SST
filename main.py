import locale
import os
import pathlib
# import inc.functions as f
# from   mDSS import mDSS
from   SST import SST

import py_dss_interface

locale.setlocale(locale.LC_NUMERIC, "pt_BR")

redes = {0: 'RedeBasica',
         1: 'Rede13Barras'}

if __name__ == "__main__":

    # Get the root folder
    script_path = os.path.dirname(os.path.abspath(__file__))

    # Get Master.dss paths
    dss_file_rede_basica = pathlib.Path(script_path).joinpath("RedeBasica", "Master.dss")
    dss_file_rede_13bus = pathlib.Path(script_path).joinpath("Rede13Barras", "Master.dss")

    # Initialize py-dss-interface
    dss = py_dss_interface.DSSDLL()

    # Compile dss file
    dss.text(f"compile [{dss_file_rede_basica}]")

    # Run solve
    dss.solution_solve()

    print(dss.circuit_total_power())

    s1 = SST(dss, 'SST1', ['barra2', 'barra3'], 1, [13.8, 0.22], 100+10j)
    s2 = SST(dss, 'SST2', ['barra2', 'barra3'], 1, [13.8, 0.22], 100+10j)

    print(SST.getAllSST())

    dss.solution_solve()
    # dssLoads.Name = 'SST1'
    # print(dssLoads.kvar)

    print(dss.circuit_total_power())
    

    
    
        
