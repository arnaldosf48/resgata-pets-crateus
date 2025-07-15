# login_window.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from cadastro_usuario import abrir_cadastro

def abrir_login(on_success):
    def tentar_login():
        email = email_entry.get()
        senha = senha_entry.get()
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE email=? AND senha=?", (email, senha))
        user = cursor.fetchone()
        conn.close()
        if user:
            root.destroy()
            on_success(user)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    root = tk.Tk()
    root.title("Login de Usuário")

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Senha").pack()
    senha_entry = tk.Entry(root, show="*")
    senha_entry.pack()

    tk.Button(root, text="Entrar", command=tentar_login).pack(pady=5)
    tk.Button(root, text="Cadastrar novo usuário", command=abrir_cadastro).pack()
    root.mainloop()
