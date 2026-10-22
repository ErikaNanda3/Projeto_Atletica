## Acessa a biblioteca nativa do Python para manipulação de data, horas, etc...
from datetime import datetime, timedelta
import email 

# ==========================================
#           CLASSES DE PESSOAS
# ==========================================
@property
class Pessoas:
    def __init__(self, nome: str, email: str = None, RA: int = None, ID: int = None):
        self.nome = nome
        self._email = email
        self.__RA = RA
        self.__ID = ID

class Alunos(Pessoas):
    def __init__(self, nome: str, email: str, RA: int, curso: str):
        super().__init__(nome = nome, email = email, RA = RA, ID = None)
        self.curso = curso
        self.__quantidadeMax = 2

class Servidores(Pessoas):
    def __init__(self, nome: str, email: str, ID: int, cargo: str):
        super().__init__(nome = nome, email = email, RA = None, ID = ID)
        self.cargo = cargo
        self.__quantidadeMax = 4

# ============================================
#       CLASSES DE EQUIPAMENTOS
# ============================================
class Equipamentos:
    def __init__(self, nome_Equipamento: str, vistoria: bool, quantidade_Equipamentos: int, descricao: str):
    
        self.nome = nome_Equipamento
        self.__vistoria = vistoria
        self.__quantidade_Equipamentos = quantidade_Equipamentos
        self.descricao = descricao

    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
    
        ## Regra Padrão (Bolas, Raquetes, Coletes): devolução até 23:59 do mesmo dia.
        return data_emprestimo.replace(hour=23, minute=59, second=59)

class Bicicletas(Equipamentos):
    def __init__(self, modelo: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = False):
    
        super().__init__(nome_Equipamento="Bicicleta",
            vistoria=vistoria,
            quantidade_Equipamentos=quantidade_Equipamentos,
            descricao=descricao
        )
    
        self.modelo = modelo

        def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
        
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

@property
class Emprestimos:
    def __init__(self, pessoa: Pessoas, equipamento: Equipamentos, data_emprestimo: datetime):
        
        self.pessoa = pessoa
        self.equipamento = equipamento
        self.data_emprestimo = data_emprestimo
        self.__data_limite = equipamento.calcular_data_limite(data_emprestimo)

    def verificar_vistoria(self, Equipamento: Equipamentos) -> bool:

        if Equipamento.__vistoria == False:        
            print(f"O equipamento {Equipamento.nome} não passou na vistoria e não pode ser emprestado.")
            print(" Fazer vistoriac agora?(digite s para sim, n para não) ")
            self.resposta = input()

            if self.resposta == "s":
                Equipamento.descricao = input("Digite a descrição da vistoria: ")
                Equipamento.__vistoria = True
                return Equipamento.__vistoria

            if self.resposta == "n":
                Equipamento.__vistoria = False
                return Equipamento.__vistoria ## vistoria não realizada, não pode emprestado.
        
        if Equipamento.__vistoria == True:
            print(f"O equipamento {Equipamento.nome} passou na vistoria e pode ser emprestado.")
            Equipamento.__vistoria = True
            return Equipamento.__vistoria
        
        
        