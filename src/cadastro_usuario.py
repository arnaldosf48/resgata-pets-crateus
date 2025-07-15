# cadastro_usuario.py
import tkinter as tk
from tkinter import messagebox
import sqlite3

def abrir_cadastro():
    def cadastrar():
        nome = nome_entry.get()
        email = email_entry.get()
        senha = senha_entry.get()

        if not (nome and email and senha):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
            win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "E-mail já cadastrado.")
        conn.close()

    win = tk.Toplevel()
    win.title("Cadastro de Usuário")

    tk.Label(win, text="Nome").pack()
    nome_entry = tk.Entry(win)
    nome_entry.pack()

    tk.Label(win, text="Email").pack()
    email_entry = tk.Entry(win)
    email_entry.pack()

    tk.Label(win, text="Senha").pack()
    senha_entry = tk.Entry(win, show="*")
    senha_entry.pack()

    tk.Button(win, text="Cadastrar", command=cadastrar).pack()
