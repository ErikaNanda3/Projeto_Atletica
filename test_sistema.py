import unittest
from datetime import datetime, timedelta

from solucao_atletica import (
    Alunos,
    Bicicletas,
    Bolas,
    Coletes,
    DadosInvalidosError,
    EquipamentoIndisponivelError,
    LimiteEmprestimosError,
    PessoaSuspensaError,
    Raquetes,
    Servidores,
    Sistema,
    VistoriaPendenteError,
)


class TestRegrasDoSistema(unittest.TestCase):
    def setUp(self):
        self.sistema = Sistema()
        self.agora = datetime(2026, 10, 20, 10, 30)
        self.aluno = Alunos("Ana", "ana@alunos.utfpr.edu.br", 111, "Computação")
        self.servidor = Servidores("Bia", "bia@alunos.utfpr.edu.br", 222, "Técnica")

    def test_prazos_de_todos_os_equipamentos(self):
        casos = [
            (Bolas("Futsal", 1, "Teste"), datetime(2026, 10, 20, 23, 59, 59)),
            (Coletes("Verde", 1, "Teste"), datetime(2026, 10, 20, 23, 59, 59)),
            (Raquetes("Tênis de mesa", 1, "Teste"), datetime(2026, 10, 22, 23, 59, 59)),
            (Bicicletas("Urbana", 1, "Teste"), datetime(2026, 10, 27, 23, 59, 59)),
        ]
        for equipamento, prazo_esperado in casos:
            with self.subTest(tipo=equipamento.nome):
                # 2 dias de atraso + 2 dias adicionais de suspensão
                self.assertEqual(equipamento.calcular_data_limite(self.agora), prazo_esperado)

    def test_limites_de_alunos_e_servidores(self):
        aluno_bolas = [Bolas(f"Bola {i}", 1, "Teste") for i in range(3)]
        for equipamento in aluno_bolas[:2]:
            self.sistema.emprestar(self.aluno, equipamento, self.agora)
        with self.assertRaises(LimiteEmprestimosError):
            self.sistema.emprestar(self.aluno, aluno_bolas[2], self.agora)

        servidor_bolas = [Bolas(f"Bola {i}", 1, "Teste") for i in range(5)]
        for equipamento in servidor_bolas[:4]:
            self.sistema.emprestar(self.servidor, equipamento, self.agora)
        with self.assertRaises(LimiteEmprestimosError):
            self.sistema.emprestar(self.servidor, servidor_bolas[4], self.agora)

    def test_estoque_e_devolucao(self):
        bola = Bolas("Futsal", 1, "Teste")
        emprestimo = self.sistema.emprestar(self.aluno, bola, self.agora)
        self.assertEqual(bola.disponiveis, 0)
        self.sistema.devolver(emprestimo, self.agora + timedelta(hours=1))
        self.assertEqual(bola.disponiveis, 1)
        self.assertFalse(emprestimo.ativo)

    def test_nao_permite_emprestar_sem_estoque(self):
        bola = Bolas("Futsal", 1, "Teste")
        self.sistema.emprestar(self.aluno, bola, self.agora)
        with self.assertRaises(EquipamentoIndisponivelError):
            self.sistema.emprestar(self.servidor, bola, self.agora)

    def test_nao_permite_emprestar_equipamento_sem_vistoria(self):
        bicicleta = Bicicletas("Urbana", 1, "Teste", vistoria=False)
        with self.assertRaises(VistoriaPendenteError):
            self.sistema.emprestar(self.aluno, bicicleta, self.agora)

    def test_atraso_aplica_suspensao_e_impede_novo_emprestimo(self):
        bola = Bolas("Futsal", 1, "Teste")
        emprestimo = self.sistema.emprestar(self.aluno, bola, self.agora)
        devolucao = datetime(2026, 10, 22, 9)
        dias_suspensao = self.sistema.devolver(emprestimo, devolucao)
        self.assertEqual(dias_suspensao, 4)
        with self.assertRaises(PessoaSuspensaError):
            self.sistema.emprestar(self.aluno, bola, devolucao)

    def test_validacao_de_email_identificadores_e_quantidade(self):
        with self.assertRaises(DadosInvalidosError):
            Alunos("Ana", 123, 111, "Computação")
        with self.assertRaises(DadosInvalidosError):
            Alunos("Ana", "ana@alunos.utfpr.edu.br", 0, "Computação")
        with self.assertRaises(DadosInvalidosError):
            Servidores("Bia", "bia@alunos.utfpr.edu.br", -1, "Técnica")
        with self.assertRaises(DadosInvalidosError):
            Bolas("Futsal", True, "Teste")

    def test_alterar_quantidade_preserva_estoque_com_unidades_emprestadas(self):
        bola = Bolas("Futsal", 2, "Teste")
        self.sistema.emprestar(self.aluno, bola, self.agora)
        bola.quantidade = 3
        self.assertEqual(bola.disponiveis, 2)
        with self.assertRaises(DadosInvalidosError):
            bola.quantidade = 0


if __name__ == "__main__":
    unittest.main()
