import locale, os
import inc.functions as f
from   mDSS import mDSS
from   SST import SST

locale.setlocale(locale.LC_NUMERIC, "pt_BR")

if __name__ == "__main__":
    
    # Inicia o OpenDSS
    # 0 - Rede Básica
    # 1 - Rede 13 Barras
    dssObj = mDSS(os.getcwd() + "\\" + f.setRede(0) + "\\Master.dss")  
    
    # Configuração das variáveis dos elementos
    obj                = dssObj.dssObj    
    dssText            = dssObj.dssText
    dssCircuit         = dssObj.dssCircuit
    dssCktElement      = dssObj.dssCktElement
    dssBus             = dssObj.dssBus
    dssLines           = dssObj.dssLines
    dssLoads           = dssObj.dssLoads
    dssTransformers    = dssObj.dssTransformers
    dssMonitors        = dssObj.dssMonitors
    dssSolution        = dssObj.dssSolution
    dssLinesCodes      = dssObj.dssLineCodes
    dssLoadShapes      = dssObj.dssLoadShapes
    
    print(dssObj.compila_DSS())
    dssText.Command = "Solve"
    
    s = SST(dssObj, 
            'SST1', 
            ['barra2', 'barra3'], 
            1, 
            [13.8, 0.22], 
            100+10j)
    
    print(s.getAllSST())
    
    dssLoads.Name = 'SST1'
    print(dssLoads.kvar)
    

    
    
        
