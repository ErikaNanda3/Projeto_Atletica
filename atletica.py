## Acessa a biblioteca nativa do Python para manipulação de data, horas, etc...
from datetime import datetime, timedelta 

# ==========================================
# CLASSES DE PESSOAS
# ==========================================
class Pessoas:
    def __init__(self, nome: str, RA: int = None, ID: int = None):
        self.nome = nome
        self.RA = RA
        self.ID = ID

class Alunos(Pessoas):
    def __init__(self, nome: str, RA: int, curso: str):
        super().__init__(nome=nome, RA=RA, ID=None)
        self.curso = curso
        self.quantidadeMax = 2

class Servidores(Pessoas):
    def __init__(self, nome: str, ID: int, cargo: str):
        super().__init__(nome=nome, RA=None, ID=ID)
        self.cargo = cargo
        self.quantidadeMax = 4

# ==========================================
# CLASSES DE EQUIPAMENTOS
# ==========================================
class Equipamentos:
    def __init__(self, nome_Equipamento: str, vistoria: bool, quantidade_Equipamentos: int, descricao: str):
        self.nome = nome_Equipamento
        self.vistoria = vistoria
        self.quantidade_Equipamentos = quantidade_Equipamentos
        self.descricao = descricao

    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
        ## Regra Padrão (Bolas, Raquetes, Coletes): devolução até 23:59 do mesmo dia.
        return data_emprestimo.replace(hour=23, minute=59, second=59)

class Bicicletas(Equipamentos):
    def __init__(self, modelo: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = False):
        super().__init__(
            nome_Equipamento="Bicicleta",
            vistoria=vistoria,
            quantidade_Equipamentos=quantidade_Equipamentos,
            descricao=descricao
        )
        self.modelo = modelo

    def data_limite(self, data_emprestimo: datetime) -> datetime:
    ## Sobrescreve a regra: devolução em até 7 dias (às 23:59 do 7º dia).
        data_limite = data_emprestimo + timedelta(days=7)
        return data_limite.replace(hour=23, minute=59, second = 59)
class Bolas(Equipamentos):
    def __init__(self, tipo_bola: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = False):
        super().__init__("Bola", vistoria, quantidade_Equipamentos, descricao)
        self.tipo_bola = tipo_bola


class Raquetes(Equipamentos):
    def __init__(self, tipo_raquete: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = False):
        super().__init__("Raquete", vistoria, quantidade_Equipamentos, descricao)
        self.tipo_raquete = tipo_raquete


class Coletes(Equipamentos):
    def __init__(self, tipo_colete: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = False):
        super().__init__("Colete", vistoria, quantidade_Equipamentos, descricao)
        self.tipo_colete = tipo_colete


