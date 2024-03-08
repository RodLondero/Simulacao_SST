# -*- coding: utf-8 -*-

class LoadShapes(object):
    """Classe para manipular as Loads"""

    def __init__(self, dssLoadShapes):
        self.dssLoadShapes = dssLoadShapes

    def Name(self, Nome_LoadShape: str = None):
        if Nome_LoadShape is None:
            return self.dssLoadShapes.Name
        else:
            self.dssLoadShapes.Name = Nome_LoadShape
            return self.dssLoadShapes.Name

    def Pmult(self, pmult: str = None):
        if pmult is not None:
            self.Pmult = pmult
        return self.dssLoadShapes.Pmult

    def Npts(self, npts: int = None):
        if npts is not None:
            self.Npts = npts
        return self.dssLoadShapes.Npts


    def PlotLoadShape(self, Nome_LoadShape: str):
        self.Name(Nome_LoadShape)
        mult = self.Pmult()

        return mult
