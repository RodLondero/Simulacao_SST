import locale, os

locale.setlocale(locale.LC_NUMERIC, "pt_BR")

from mDSS import mDSS

if __name__ == "__main__":
           
    dssObj = mDSS(os.getcwd() + "\\13Barras\\Master.dss")  
    
    obj                = dssObj.dssObj
    dssText            = dssObj.dssText
    dssCircuit         = dssObj.dssCircuit
    dssCktElement      = dssObj.dssCktElement
    dssBus             = dssObj.dssBus
    dssLines           = dssObj.dssLines
    dssLoads           = dssObj.dssLines
    dssTransformers    = dssObj.dssTransformers
    dssMonitors        = dssObj.dssMonitors
    dssSolution        = dssObj.dssSolution
    dssLinesCodes      = dssObj.dssLineCodes
    dssLoadShapes      = dssObj.dssLoadShapes
    

    
    
        
