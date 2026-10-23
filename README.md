# Sistema de Empréstimo de Equipamentos Esportivos

Trabalho da disciplina de **Programação Orientada a Objetos (POO)**, desenvolvido em **Python** e **Java** por estudantes de **Engenharia de Computação** da **UTFPR – Campus Apucarana**.

## Equipe

- Érika Fernanda Souza
- Tarsila Paiva Pimentel
- Emilly de Oliveira Siqueira

## Sobre o projeto

Sistema em linha de comando (terminal) para gerenciar o empréstimo de equipamentos esportivos de um campus (bolas, raquetes, coletes e bicicletas) para **alunos** e **servidores**. O sistema controla prazos de devolução, limite de itens por pessoa, estoque, vistoria de bicicletas, histórico e punição por atraso.

## Funcionalidades

- Cadastro de alunos, servidores e equipamentos
- Registro de novo empréstimo com validação de regras
- Devolução com cálculo automático de atraso e suspensão
- Vistoria obrigatória (pneus, freios e corrente) na devolução de bicicletas
- Histórico geral ou por pessoa
- Lembretes de vencimento (atrasado, vence hoje, vence amanhã)
- Listagem de equipamentos e de itens emprestados no momento
- Mensagens coloridas no terminal para operações bem-sucedidas

## Regras de negócio

### Limite de equipamentos por pessoa

| Tipo de pessoa | Limite |
|---|---|
| Aluno | 2 equipamentos |
| Servidor | 4 equipamentos |

### Prazo de devolução

| Equipamento | Prazo |
|---|---|
| Bola | Até o fim do mesmo dia (23:59:59) |
| Colete | Até o fim do mesmo dia (23:59:59) |
| Raquete | 2 dias (até 23:59:59) |
| Bicicleta | 7 dias (até 23:59:59) |

### Punição por atraso

Em caso de atraso, a pessoa fica suspensa e não pode realizar novos empréstimos:

```
dias de suspensão = dias de atraso + 2
```

### Outras regras

- Equipamento sem vistoria não pode ser emprestado.
- Não é possível emprestar um equipamento sem unidades disponíveis.
- Nome não pode ser vazio e o e-mail, quando informado, deve conter `@`.

## Conceitos de POO aplicados

- **Abstração**: classes abstratas `Pessoas` e `Equipamentos` (módulo `abc`).
- **Herança**: `Alunos` e `Servidores` herdam de `Pessoas`; `Bicicletas`, `Bolas`, `Raquetes` e `Coletes` herdam de `Equipamentos`.
- **Polimorfismo**: `identificador` (RA ou ID) e `calcular_data_limite` se comportam de forma diferente em cada classe.
- **Encapsulamento**: atributos privados, `@property` e setters com validação.
- **Tratamento de exceções**: hierarquia de exceções personalizadas.

## Estrutura de classes

```
Exception
└── EmprestimoError
    ├── DadosInvalidosError
    ├── EquipamentoIndisponivelError
    ├── VistoriaPendenteError
    ├── LimiteEmprestimosError
    └── PessoaSuspensaError

Pessoas (abstrata)
├── Alunos
└── Servidores

Equipamentos (abstrata)
├── Bicicletas
├── Bolas
├── Raquetes
└── Coletes

Emprestimos   -> liga uma pessoa a um equipamento
Sistema       -> concentra as regras gerais e as listas de dados
```

## Como executar

### Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa
- Terminal com suporte a cores ANSI (opcional, apenas para as mensagens verdes)

### Executar o sistema

```bash
python solucao_atletica.py
```

O comando deve ser executado no terminal, dentro da pasta do projeto. O sistema abre o menu e mantém os dados em memória até o encerramento.

### Executar os testes automatizados

Na mesma pasta, execute:

```bash
python -m unittest -v
```

## Menu do sistema

| Opção | Ação |
|---|---|
| 1 | Cadastrar aluno |
| 2 | Cadastrar servidor |
| 3 | Cadastrar equipamento |
| 4 | Novo empréstimo |
| 5 | Devolução / vistoria |
| 6 | Histórico |
| 7 | Lembretes |
| 8 | Listar equipamentos |
| 9 | Itens emprestados |
| 0 | Sair |

## Dados iniciais de teste

Ao iniciar, o sistema já carrega alguns registros para facilitar os testes:

- **Alunos**: Érika Souza (RA 123456), Tarsila (RA 654321)
- **Servidor**: Carlos Silva (ID 9876)
- **Equipamentos**: Bola de futsal (3), Raquete de tênis de mesa (2), Coletes verdes (10), Mountain bike (2)

## Observações

- Os dados ficam apenas em memória: ao encerrar o programa, tudo é perdido.
- Um resultado "Com Avarias" na vistoria da bicicleta é registrado no histórico, mas não bloqueia o equipamento.

## Instituição

Universidade Tecnológica Federal do Paraná (UTFPR) – Campus Apucarana
Curso de Engenharia de Computação
