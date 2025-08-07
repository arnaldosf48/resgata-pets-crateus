# Projeto de Testes Automatizados - Resgata Pets Crateús

## Descrição
Este projeto contém testes automatizados para a aplicação Resgata Pets Crateús, utilizando pytest. Os testes cobrem as principais funcionalidades do sistema, incluindo autenticação de usuários e gerenciamento de resgates de animais.

## Estrutura do Projeto
```
pytest-automation-project/
├── src/
│   ├── __init__.py
│   └── auth.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_resgates.py
├── requirements.txt
└── README.md
```

## Pré-requisitos
- [Python 3.10+](https://www.python.org/downloads/)
- Pip (gerenciador de pacotes do Python)

## Configuração do Ambiente

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/resgata-pets-crateus.git
cd resgata-pets-crateus/pytest-automation-project
```

2. **Configure o ambiente virtual:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## Executando os Testes

### Executar todos os testes:
```bash
pytest
```

### Executar testes específicos:
```bash
pytest tests/test_auth.py
pytest tests/test_resgates.py
```

### Executar com relatório detalhado:
```bash
pytest -v
```

## Casos de Teste

### Autenticação (`test_auth.py`)
- Cadastro de usuário
- Login de usuário
- Validação de dados de entrada

### Resgates (`test_resgates.py`)
- Registro de novo resgate
- Consulta de resgates por usuário
- Validação dos dados do resgate

## Estrutura dos Testes
Os testes seguem o padrão AAA (Arrange-Act-Assert):
- **Arrange**: Preparação do ambiente e dados
- **Act**: Execução da funcionalidade
- **Assert**: Verificação dos resultados