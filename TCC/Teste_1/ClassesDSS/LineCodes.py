# -*- coding: utf-8 -*-


class LineCodes(object):
    """"""

    def __init__(self, dssLineCodes):
        """Constructor for LineCodes"""
        self.dssLineCodes = dssLineCodes

    def set_linecode_by_name(self, Nome_LineCode: str):
        self.dssLineCodes.Name = Nome_LineCode
        return self.dssLineCodes.Name

    def AllNames(self):
        return self.dssLineCodes.AllNames

    def Name(self):
        return self.dssLineCodes.Name

    def Phases(self):
        return self.dssLineCodes.Phases


