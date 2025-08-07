import sys
import os
import pytest
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestAuth:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Arrange
        self.test_db = "test_db.sqlite3"
        self.conn = sqlite3.connect(self.test_db)
        self.cursor = self.conn.cursor()
        
        # Criar tabelas de teste
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        ''')
        
        yield
        
        # Cleanup
        self.conn.close()
        os.remove(self.test_db)

    def test_cadastro_usuario_sucesso(self):
        # Arrange
        dados_usuario = ("Teste Silva", "teste@email.com", "senha123")
        
        # Act
        self.cursor.execute('''
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
        ''', dados_usuario)
        self.conn.commit()
        
        # Assert
        self.cursor.execute('SELECT * FROM usuarios WHERE email = ?', ("teste@email.com",))
        usuario = self.cursor.fetchone()
        assert usuario is not None
        assert usuario[1] == "Teste Silva"

    def test_login_usuario_sucesso(self):
        # Arrange
        dados_usuario = ("Teste Silva", "teste@email.com", "senha123")
        self.cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', dados_usuario)
        self.conn.commit()
        
        # Act
        self.cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', 
                          ("teste@email.com", "senha123"))
        usuario = self.cursor.fetchone()
        
        # Assert
        assert usuario is not None