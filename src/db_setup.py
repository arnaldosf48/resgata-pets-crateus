import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Cria a tabela de usuários (se ainda não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')

# Cria a tabela de resgates (se ainda não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS resgates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    localizacao TEXT NOT NULL,
    responsavel TEXT NOT NULL,
    condicao TEXT NOT NULL,
    observacoes TEXT,
    imagem_path TEXT,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)
''')

conn.commit()
conn.close()

print("Banco e tabelas criados com sucesso.")
