import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from cadastro_usuario import abrir_cadastro
import os

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
    root.geometry("800x400") 
    root.resizable(False, False)

    # Frame esquerdo (branco)
    frame_esquerdo = tk.Frame(root, bg="white", width=600, height=300)
    frame_esquerdo.pack(side="left", fill="both")

    # Imagem no frame esquerdo
    imagem_path = os.path.join(os.path.dirname(__file__), "logo.png")  # Caminho da imagem 

    if os.path.exists(imagem_path):
        try:
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 200))
            imagem_tk = ImageTk.PhotoImage(imagem)
            label_imagem = tk.Label(frame_esquerdo, image=imagem_tk, bg="white")
            label_imagem.image = imagem_tk
            label_imagem.pack(expand=True)
        except Exception as e:
            tk.Label(frame_esquerdo, text=f"Erro ao carregar imagem: {e}", bg="white").pack(pady=20)
    else:
        tk.Label(frame_esquerdo, text="Imagem 'logo.png' não encontrada.\nColoque ao lado do arquivo login_window.py", bg="white").pack(pady=20)

    # Frame direito (verde)
    frame_direito = tk.Frame(root, bg="#0B2B26", width=300, height=300)
    frame_direito.pack(side="right", fill="both", expand=True)

    # Campos de login no frame direito
    tk.Label(frame_direito, text="Email", bg="#0B2B26", fg="white").pack(pady=(40, 5))
    email_entry = tk.Entry(frame_direito, width=30)
    email_entry.pack()

    tk.Label(frame_direito, text="Senha", bg="#0B2B26", fg="white").pack(pady=5)
    senha_entry = tk.Entry(frame_direito, show="*", width=30)
    senha_entry.pack()

    tk.Button(frame_direito, text="Entrar", command=tentar_login).pack(pady=10)
    tk.Button(frame_direito, text="Cadastrar novo usuário", command=abrir_cadastro).pack()

    root.mainloop()
