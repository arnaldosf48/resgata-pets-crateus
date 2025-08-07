import sys
import os
import pytest
import sqlite3
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestResgates:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Arrange
        self.test_db = "test_db.sqlite3"
        self.conn = sqlite3.connect(self.test_db)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS resgates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            condicao TEXT NOT NULL,
            observacoes TEXT,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
        ''')
        
        # Inserir usuário de teste
        self.cursor.execute('''
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
        ''', ("Teste Silva", "teste@email.com", "senha123"))
        self.conn.commit()
        
        yield
        
        # Cleanup
        self.conn.close()
        os.remove(self.test_db)

    def test_cadastro_resgate_sucesso(self):
        # Arrange
        self.cursor.execute('SELECT id FROM usuarios WHERE email = ?', ("teste@email.com",))
        usuario_id = self.cursor.fetchone()[0]
        
        dados_resgate = (
            "Cachorro",
            datetime.now().strftime("%d/%m/%Y"),
            datetime.now().strftime("%H:%M"),
            "Rua Teste, 123",
            "João Responsável",
            "Bom estado",
            "Animal dócil",
            usuario_id
        )
        
        # Act
        self.cursor.execute('''
            INSERT INTO resgates (tipo, data, hora, localizacao, responsavel, condicao, observacoes, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', dados_resgate)
        self.conn.commit()
        
        # Assert
        self.cursor.execute('SELECT * FROM resgates WHERE usuario_id = ?', (usuario_id,))
        resgate = self.cursor.fetchone()
        assert resgate is not None
        assert resgate[1] == "Cachorro"

    def test_buscar_resgates_usuario(self):
        # Arrange
        self.cursor.execute('SELECT id FROM usuarios WHERE email = ?', ("teste@email.com",))
        usuario_id = self.cursor.fetchone()[0]
        
        dados_resgate = (
            "Cachorro",
            datetime.now().strftime("%d/%m/%Y"),
            datetime.now().strftime("%H:%M"),
            "Rua Teste, 123",
            "João Responsável",
            "Bom estado",
            "Animal dócil",
            usuario_id
        )
        
        self.cursor.execute('''
            INSERT INTO resgates (tipo, data, hora, localizacao, responsavel, condicao, observacoes, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', dados_resgate)
        self.conn.commit()
        
        # Act
        self.cursor.execute('SELECT * FROM resgates WHERE usuario_id = ?', (usuario_id,))
        resgates = self.cursor.fetchall()
        
        # Assert
        assert len(resgates) == 1
        assert resgates[0][1] == "Cachorro"