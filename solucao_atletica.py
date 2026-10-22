from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Cores para o terminal
COR_VERDE = "\033[92m"
COR_RESET = "\033[0m"

DIAS_EXTRA_PUNICAO = 2  # punição = dias de atraso + 2 dias sem poder emprestar


# ==========================================
#        EXCEÇÕES PERSONALIZADAS
# ==========================================
class EmprestimoError(Exception):
    """Erro base do sistema (capturando este, captura todos os de baixo)."""
class DadosInvalidosError(EmprestimoError):
    pass
class EquipamentoIndisponivelError(EmprestimoError):
    pass
class VistoriaPendenteError(EmprestimoError):
    pass
class LimiteEmprestimosError(EmprestimoError):
    pass
class PessoaSuspensaError(EmprestimoError):
    pass


# ==========================================
#           CLASSES DE PESSOAS
# ==========================================
class Pessoas(ABC): # Classe abstrata, serve como molde OBRIGATÓRIO para as classes filhas
    _limite_max = 1

    def __init__(self, nome: str, email: str = None):
        self.nome = nome
        self.email = email
        self.__suspenso_ate = None
        self._emprestimos_ativos = []

    # ---- getter e setter de nome ----
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DadosInvalidosError("O nome não pode ser vazio.")
        self.__nome = valor.strip()

    # ---- getter e setter de email ----
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if valor is not None and "@" not in valor:
            raise DadosInvalidosError("E-mail inválido (falta o @).")
        self._email = valor

    # ---- somente leitura (só getter, sem setter) ----
    @property
    def limite_max(self) -> int:
        return self._limite_max

    @property
    def suspenso_ate(self):
        return self.__suspenso_ate

    @property
    @abstractmethod
    def identificador(self):
        pass

    # ---- regras ----
    def esta_suspenso(self, agora: datetime) -> bool:
        return self.__suspenso_ate is not None and agora < self.__suspenso_ate

    def suspender(self, ate: datetime):
        self.__suspenso_ate = ate

    def verificar_pode_emprestar(self, agora: datetime):
        if self.esta_suspenso(agora):
            raise PessoaSuspensaError(
                f"{self.nome} está suspenso(a) até "
                f"{self.__suspenso_ate:%d/%m/%Y %H:%M} por atraso."
            )
        if len(self._emprestimos_ativos) >= self._limite_max:
            raise LimiteEmprestimosError(
                f"{self.nome} já está com o limite de {self._limite_max} equipamento(s)."
            )

    def __str__(self):
        return f"{self.nome} ({self.identificador})"


class Alunos(Pessoas):
    _limite_max = 2

    def __init__(self, nome: str, email: str, RA: int, curso: str):
        super().__init__(nome, email)
        self.__RA = RA
        self.curso = curso

    @property
    def RA(self) -> int:
        return self.__RA

    @property
    def identificador(self) -> int:
        return self.__RA


class Servidores(Pessoas):
    _limite_max = 4

    def __init__(self, nome: str, email: str, ID: int, cargo: str):
        super().__init__(nome, email)
        self.__ID = ID
        self.cargo = cargo

    @property
    def ID(self) -> int:
        return self.__ID

    @property
    def identificador(self) -> int:
        return self.__ID


# ============================================
#       CLASSES DE EQUIPAMENTOS
# ============================================
class Equipamentos(ABC): # ADD: Herda de ABC para poder ter método abstrato
    def __init__(self, nome_Equipamento: str, vistoria: bool, quantidade_Equipamentos: int, descricao: str):
        self.__nome = nome_Equipamento
        self.vistoria = vistoria                        # usa o setter
        self.__total = 0
        self.quantidade = quantidade_Equipamentos       # usa o setter
        self.__disponiveis = self.__total
        self.descricao = descricao

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def vistoria(self) -> bool:
        return self.__vistoria

    @vistoria.setter
    def vistoria(self, valor: bool):
        if not isinstance(valor, bool):
            raise DadosInvalidosError("Vistoria deve ser True ou False.")
        self.__vistoria = valor

    @property
    def quantidade(self) -> int:
        return self.__total

    @quantidade.setter
    def quantidade(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise DadosInvalidosError("Quantidade deve ser um inteiro >= 0.")
        self.__total = valor

    @property
    def disponiveis(self) -> int:
        return self.__disponiveis

    def realizar_vistoria(self, descricao: str):
        self.descricao = descricao
        self.__vistoria = True

    def retirar_unidade(self):
        if not self.__vistoria:
            raise VistoriaPendenteError(
                f"O equipamento {self.nome} não passou na vistoria e não pode ser emprestado."
            )
        if self.__disponiveis <= 0:
            raise EquipamentoIndisponivelError(f"Não há {self.nome} disponível.")
        self.__disponiveis -= 1

    def devolver_unidade(self):
        if self.__disponiveis >= self.__total:
            raise EquipamentoIndisponivelError("Todas as unidades já estão no estoque.")
        self.__disponiveis += 1

    @abstractmethod
    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
        pass

    def __str__(self):
        status = "vistoriado" if self.__vistoria else "SEM vistoria"
        return f"{self.nome} - {self.descricao} [{self.__disponiveis}/{self.__total}, {status}]"


class Bicicletas(Equipamentos):
    def __init__(self, modelo: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = True):
        super().__init__("Bicicleta", vistoria, quantidade_Equipamentos, descricao)
        self.modelo = modelo

    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
        limite = data_emprestimo + timedelta(days=7)
        return limite.replace(hour=23, minute=59, second=59)


class Bolas(Equipamentos):
    def __init__(self, tipo_bola: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = True):
        super().__init__("Bola", vistoria, quantidade_Equipamentos, descricao)
        self.tipo_bola = tipo_bola

    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:      
        return data_emprestimo.replace(hour=23, minute=59, second=59)


class Raquetes(Equipamentos):
    def __init__(self, tipo_raquete: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = True):
        super().__init__("Raquete", vistoria, quantidade_Equipamentos, descricao)
        self.tipo_raquete = tipo_raquete
    
    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
        limite = data_emprestimo + timedelta(days=2) 
        return limite.replace(hour=23, minute=59, second=59)


class Coletes(Equipamentos):
    def __init__(self, tipo_colete: str, quantidade_Equipamentos: int, descricao: str, vistoria: bool = True):
        super().__init__("Colete", vistoria, quantidade_Equipamentos, descricao)
        self.tipo_colete = tipo_colete

    def calcular_data_limite(self, data_emprestimo: datetime) -> datetime:
        return data_emprestimo.replace(hour=23, minute=59, second=59)


# ============================================
#                EMPRÉSTIMOS
# ============================================
class Emprestimos:
    def __init__(self, pessoa: Pessoas, equipamento: Equipamentos, data_emprestimo: datetime):
        self.pessoa = pessoa
        self.equipamento = equipamento
        self.data_emprestimo = data_emprestimo
        self.__data_limite = equipamento.calcular_data_limite(data_emprestimo)
        self.__data_devolucao = None
        self.__dias_punicao = 0   # fica registrado para o histórico
        self.__vistoria = ""

    @property
    def dias_punicao(self) -> int:
        return self.__dias_punicao

    @property
    def data_limite(self) -> datetime:
        return self.__data_limite

    @property
    def data_devolucao(self):
        return self.__data_devolucao

    @property
    def ativo(self) -> bool:
        return self.__data_devolucao is None

    def dias_atraso(self, referencia: datetime) -> int:
        fim = self.__data_devolucao or referencia
        return max(0, (fim.date() - self.__data_limite.date()).days)

    def registrar_devolucao(self, data: datetime, vistoria: str = "") -> int:
        """Devolve o equipamento e aplica a punição. Retorna os dias de suspensão."""
        if not self.ativo:
            raise EmprestimoError("Este empréstimo já foi devolvido.")
        self.__data_devolucao = data
        self.__vistoria = vistoria
        self.equipamento.devolver_unidade()
        self.pessoa._emprestimos_ativos.remove(self)

        atraso = self.dias_atraso(data)
        if atraso > 0:
            dias_punicao = atraso + DIAS_EXTRA_PUNICAO
            self.__dias_punicao = dias_punicao
            self.pessoa.suspender(data + timedelta(days=dias_punicao))
            return dias_punicao
        return 0

    def linha_historico(self) -> str:
        """Uma linha do histórico: quem pegou, o quê, quando e como terminou."""
        base = (f"{self.data_emprestimo:%d/%m/%Y %H:%M} | {self.pessoa.nome} | "
                f"{self.equipamento.nome} | prazo {self.__data_limite:%d/%m/%Y} | ")
        if self.ativo:
            return base + f"EM ABERTO (Prazo: {self.__data_limite:%d/%m/%Y})"
        atraso = self.dias_atraso(self.__data_devolucao)
        vistoria_info = f" [Vistoria: {self.__vistoria}]" if self.__vistoria else ""
        if atraso:
            return (base + f"devolvido {self.__data_devolucao:%d/%m/%Y %H:%M} "
                    f"com {atraso} dia(s) de atraso (suspensão de {self.__dias_punicao} dia(s)){vistoria_info}")
        return base + f"devolvido {self.__data_devolucao:%d/%m/%Y %H:%M} no prazo{vistoria_info}"

    def __str__(self):
        return (f"{self.equipamento.nome} com {self.pessoa.nome} "
                f"(devolver até {self.__data_limite:%d/%m/%Y %H:%M})")


# ============================================
#           SISTEMA (regras gerais)
# ============================================
class Sistema:
    def __init__(self):
        self.pessoas = []
        self.equipamentos = []
        self.emprestimos = []
        self._carregar_dados_iniciais()  # ADD: Chamando para iniciar com dados de teste!

    def _carregar_dados_iniciais(self):
        # Alunos e servidores iniciais
        self.pessoas.append(Alunos("Érika Souza", "erika@email.com", 123456, "Engenharia"))
        self.pessoas.append(Alunos("Vinicius Pires", "vinicius@email.com", 654321, "Computação"))
        self.pessoas.append(Servidores("Carlos Silva", "carlos@campus.br", 9876, "Técnico"))

        self.equipamentos.append(Bolas("Futsal", 3, "Penalty Oficial"))
        self.equipamentos.append(Raquetes("Tênis de Mesa", 2, "Kuna Pro"))
        self.equipamentos.append(Coletes("Verde", 10, "Treino"))
        self.equipamentos.append(Bicicletas("Mountain Bike", 2, "Aro 29 Reitoria"))

    def emprestar(self, pessoa, equipamento, agora=None) -> Emprestimos:
        agora = agora or datetime.now()
        pessoa.verificar_pode_emprestar(agora)
        equipamento.retirar_unidade()
        emp = Emprestimos(pessoa, equipamento, agora)
        pessoa._emprestimos_ativos.append(emp)
        self.emprestimos.append(emp)
        return emp

    def devolver(self, emprestimo, agora=None, vistoria: str = "") -> int:
        return emprestimo.registrar_devolucao(agora or datetime.now(), vistoria)

    def ativos(self):
        return [e for e in self.emprestimos if e.ativo]

    def historico(self, pessoa=None) -> list:
        lista = [e for e in self.emprestimos if pessoa is None or e.pessoa is pessoa]
        return [e.linha_historico() for e in reversed(lista)]

    def lembretes(self, agora=None) -> list:
        agora = agora or datetime.now()
        msgs = []
        for e in self.ativos():
            dias = (e.data_limite.date() - agora.date()).days
            if dias < 0:
                msgs.append(f"ATRASADO ({-dias} dia(s)): {e}")
            elif dias == 0:
                msgs.append(f"VENCE HOJE: {e}")
            elif dias == 1:
                msgs.append(f"Vence amanhã: {e}")
        return msgs


# ============================================
#                   MENU
# ============================================
def ler_inteiro(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")


def escolher(lista, titulo: str):
    if not lista:
        raise EmprestimoError("Nenhum registro encontrado.")
    for i, item in enumerate(lista, 1):
        print(f"  {i} - {item}")
    pos = ler_inteiro(titulo)
    if not 1 <= pos <= len(lista):
        raise DadosInvalidosError("Opção fora da lista.")
    return lista[pos - 1]


def cadastrar_equipamento(sistema):
    print("1-Bicicleta  2-Bola  3-Raquete  4-Colete")
    tipo = ler_inteiro("Tipo: ")
    sub = input("Modelo/tipo: ")
    qtd = ler_inteiro("Quantidade: ")
    desc = input("Descrição: ")
    classes = {1: Bicicletas, 2: Bolas, 3: Raquetes, 4: Coletes}
    if tipo not in classes:
        raise DadosInvalidosError("Tipo de equipamento inválido.")
    sistema.equipamentos.append(classes[tipo](sub, qtd, desc))
    print(f"{COR_VERDE}Equipamento cadastrado com sucesso!{COR_RESET}")


def menu():
    sistema = Sistema()
    for aviso in sistema.lembretes():
        print(">>", aviso)

    while True:
        print("\n ============================================================")
        print("                               MENU ")
        print(" ============================================================")
        print("| 1-Cadastrar aluno    | 2-Cadastrar servidor   | 3-Cadastrar equipamento")
        print("| 4-Novo Emprestimo    | 5-Devolução/Vistoria   | 6-Histórico")
        print("| 7-Lembretes          | 8-Listar equipamentos  | 9-Itens emprestados")
        print("0-Sair")
        opcao = input("Opção: ").strip()

        try:
            if opcao == "1":
                sistema.pessoas.append(Alunos(input("Nome: "), input("E-mail: "), ler_inteiro("RA: "), input("Curso: ")))
                print(f"{COR_VERDE}Aluno cadastrado com sucesso!{COR_RESET}")

            elif opcao == "2":
                sistema.pessoas.append(Servidores(input("Nome: "), input("E-mail: "), ler_inteiro("ID: "), input("Cargo: ")))
                print(f"{COR_VERDE}Servidor cadastrado com sucesso!{COR_RESET}")

            elif opcao == "3":
                cadastrar_equipamento(sistema)

            elif opcao == "4":
                print("\n-- Selecione a Pessoa --")
                pessoa = escolher(sistema.pessoas, "Número da pessoa: ")
                print("\n-- Selecione o Equipamento --")
                eq = escolher(sistema.equipamentos, "Número do equipamento: ")
                emp = sistema.emprestar(pessoa, eq)
                print(f"{COR_VERDE}Empréstimo realizado com sucesso! Devolver até {emp.data_limite:%d/%m/%Y %H:%M}.{COR_RESET}")

            elif opcao == "5":
                print("\n-- Empréstimos Ativos --")
                emp = escolher(sistema.ativos(), "Selecione o empréstimo a devolver: ")
                
                obs_vistoria = ""
                # Vistoria obrigatória da bicicleta (requisito do PDF)
                if isinstance(emp.equipamento, Bicicletas):
                    print("\n[Vistoria Obrigatória da Bicicleta]")
                    pneu = input("Pneus em bom estado? (s/n): ").strip().lower() == "s"
                    freio = input("Freios funcionando? (s/n): ").strip().lower() == "s"
                    corrente = input("Corrente lubrificada e ajustada? (s/n): ").strip().lower() == "s"
                    status = "Aprovada" if (pneu and freio and corrente) else "Com Avarias"
                    obs_vistoria = f"Pneu:{'OK' if pneu else 'NOK'}, Freio:{'OK' if freio else 'NOK'}, Corrente:{'OK' if corrente else 'NOK'} ({status})"

                punicao = sistema.devolver(emp, vistoria = obs_vistoria)
                if punicao:
                    print(f"Devolução realizada com ATRASO! {emp.pessoa.nome} fica suspenso(a) por {punicao} dia(s).")
                else:
                    print(f"{COR_VERDE}Devolvido no prazo com sucesso! Obrigado.{COR_RESET}")

            elif opcao == "6":
                print("\n-- Histórico de Empréstimos --")
                filtro = input("Histórico de uma pessoa específica? (s = sim / Enter = geral): ").strip().lower()
                pessoa = escolher(sistema.pessoas, "Pessoa: ") if filtro == "s" else None
                print("\n".join(sistema.historico(pessoa)) or "Histórico vazio.")

            elif opcao == "7":
                print("\n-- Lembretes de Vencimento --")
                print("\n".join(sistema.lembretes()) or "Nenhum lembrete no momento.")

            elif opcao == "8":
                print("\n-- Lista de Equipamentos --")
                print("\n".join(str(e) for e in sistema.equipamentos) or "Nenhum equipamento cadastrado.")

            elif opcao == "9":
                print("\n-- Equipamentos Emprestados no Momento --")
                ativos = sistema.ativos()
                if not ativos:
                    print("Nenhum item emprestado no momento.")
                for emp in ativos:
                    print(f"- {emp.equipamento.nome} ({emp.equipamento.descricao}) -> com {emp.pessoa.nome} [Até: {emp.data_limite:%d/%m/%Y}]")

            elif opcao == "0":
                print("Até mais!")
                break
            else:
                print("Opção inválida.")

        except EmprestimoError as erro:
            print(f"[Não foi possível] {erro}")
        except Exception as erro:
            print(f"[Erro inesperado] {erro}")


if __name__ == "__main__":
    menu()