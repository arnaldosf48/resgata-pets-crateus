# 🐾 Sistema de Gerenciamento de Resgates de Animais

Este sistema foi desenvolvido para registrar, organizar e permitir o gerenciamento de informações relacionadas a **resgates de animais**, atendendo a necessidades de equipes de resgate, ONGs, voluntários ou órgãos públicos.

---

## 📌 Objetivo

Facilitar o **controle, histórico e análise** dos resgates realizados, por meio de um sistema desktop local, leve e intuitivo, que **não depende de conexão com a internet**.

---

## 🖥️ Tecnologias Utilizadas

- **Python 3.7+**
- **Tkinter** – Interface gráfica
- **SQLite** – Banco de dados local
- **FPDF** – Exportação de relatórios em PDF

---

## 🚀 Funcionalidades

### ✅ Funcionais

- Cadastro de resgates com:
  - Tipo do animal
  - Data e hora
  - Localização
  - Responsável
  - Condição e observações
- Listagem em tabela com filtros por:
  - Tipo de animal
  - Data
  - Responsável
- Edição e exclusão de registros
- Exportação da lista de resgates para **PDF**
- Cadastro e login de usuários
- Restrição de acesso para usuários autenticados
- Logout

### ✅ Não Funcionais

- Interface gráfica simples e intuitiva
- Armazenamento local com persistência automática
- Compatível com Windows (opcionalmente Linux)
- Baixo consumo de recursos

---

# 🐾 Resgata Pet Crateús - Guia de Execução

Este é um guia passo a passo para rodar o sistema de cadastro e gerenciamento de usuários do projeto **Resgata Pet Crateús**.

---

## ✅ Requisitos

Antes de iniciar, é necessário ter instalado:

- [Python 3.10+](https://www.python.org/downloads/)
- Pip (gerenciador de pacotes do Python)

Verifique com os comandos:

```bash
python --version
pip --version
```

---


## 📦 Passo 1 - Instalar dependências

Execute no terminal:

```bash
pip install pillow fpdf matplotlib
```

---

## Passo 2 Clonando o Repositório

Abra o terminal e execute:

```sh
git clone https://github.com/arnaldosf48/resgata-pets-crateus.git
cd resgata-pets-crateus
```

### Estrutura esperada do projeto

Os arquivos estarao organizados da seguinte forma:

```
resgata-pet-crateus/
│
├── src/
│   ├── main.py
│   ├── login_window.py
│   ├── dashboard_window.py
│   ├── db_setup.py
│   └── ... outros arquivos
│
└── db.sqlite3   ← banco de dados SQLite
```

---

## Passo 3 - Criar o banco de dados (se ainda não existir)

Crie o arquivo `db.sqlite3` executando o `db_setup.py` ou pelo terminal:

```bash
cd src
python db_setup.py
```

---

## ▶️ Passo 4 - Rodar o sistema

Acesse a pasta onde está o `main.py` e execute:

```bash
cd src
python main.py
```

---

## Problemas comuns

- `ModuleNotFoundError`: instale os pacotes com `pip install <nome-do-pacote>`
- `sqlite3.OperationalError`: verifique se o banco foi criado corretamente
- O sistema precisa ser executado em um ambiente com interface gráfica (Windows ou Linux Desktop)

---

## Observação

Este projeto usa **Tkinter** como interface gráfica, além de bibliotecas externas como **Pillow**, **FPDF** e **Matplotlib**.
