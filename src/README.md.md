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
- Exibição do nome e e-mail do usuário logado
- Restrição de acesso para usuários autenticados
- Logout

### ✅ Não Funcionais

- Interface gráfica simples e intuitiva
- Armazenamento local com persistência automática
- Compatível com Windows (opcionalmente Linux)
- Pode ser transformado em `.exe` para instalação offline
- Baixo consumo de recursos

---

## 📁 Estrutura do Projeto

```
resgates_animais/
│
├── main.py                  # Arquivo principal
├── db_setup.py              # Criação das tabelas no SQLite
├── login_window.py          # Tela de login e cadastro de usuário
├── dashboard_window.py      # Tela principal após login
├── db.sqlite3               # Banco de dados local (gerado após o setup)
└── README.md                # Documentação do projeto
```

---

## ⚙️ Como Executar

1. Instale o Python 3: [https://www.python.org/downloads](https://www.python.org/downloads)

2. Instale as dependências:

```bash
pip install fpdf
```

3. Crie o banco de dados local (roda apenas uma vez):

```bash
python db_setup.py
```

4. Inicie a aplicação:

```bash
python main.py
```

---

## 📦 Empacotamento como Executável (Windows)

Instale o PyInstaller:

```bash
pip install pyinstaller
```

Gere o `.exe`:

```bash
pyinstaller --noconsole --onefile main.py
```

O executável será gerado em:

```
dist/main.exe
```

---

## 👥 Equipe de Desenvolvimento

- **Arnaldo Filho** – Analista e Desenvolvedor
- [Adicionar demais membros se houver]

---

## 🐛 Suporte e Feedback

Caso encontre erros ou tenha sugestões, entre em contato com a equipe ou abra uma issue no repositório.

---

## 📄 Licença

Este projeto é de uso acadêmico e sem fins lucrativos. Licença livre para fins educativos e não comerciais.