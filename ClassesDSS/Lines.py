# -*- coding: utf-8 -*-


class Lines(object):

    def __init__(self, dssLines):
        self.dssLines = dssLines

# =============================================================================
#   Linhas
# =============================================================================
    def set_linha_by_name(self, Nome_Linha: str):
        self.dssLines.Name = Nome_Linha
        return  self.dssLines.Name

    def get_nome_linha(self):
        return self.dssLines.Name

    def tamanho(self, tamanho: float = None):
        if tamanho is None:
            return self.dssLines.Length
        else:
            self.dssLines.Length = tamanho
            return self.dssLines.Length

    def get_nome_e_tamanho_linhas(self):
        # Definindo duas listas
        nome_linhas_lista = []
        tamanho_linhas_lista = []

        # Seleciona a primeira linha
        self.dssLines.First

        for i in range(self.dssLines.Count):

            # print("TESTE ELEMENTO ATIVO: " + self.dssCktElement.Name)
            # print("TENSÃO NO ELEMENTO ATIVO: "
            #       + str(self.dssCktElement.VoltagesMagAng))

            nome_linhas_lista.append(self.dssLines.Name)
            tamanho_linhas_lista.append(self.dssLines.Length)

            self.dssLines.Next

        return nome_linhas_lista, tamanho_linhas_lista
