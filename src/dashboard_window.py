# dashboard_window.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from fpdf import FPDF
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt



def abrir_dashboard(usuario):
    root = tk.Tk()
    root.title("Sistema de Resgates de Animais")
    root.configure(bg="#0B2B26")

    # Texto de usuário logado
    tk.Label(root, text=f"Usuário logado: {usuario[1]} ({usuario[2]})", fg="white", bg="#0B2B26", font=("Arial", 10, "bold")).pack(pady=5)

    frame_up = tk.Frame(root, bg="white", width=600, height=300)
    frame_up.pack(side="left", fill="both")
    imagem_path = os.path.join(os.path.dirname(__file__), "logo2.png")  # Caminho da imagem 

    if os.path.exists(imagem_path):
        try:
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 400))
            imagem_tk = ImageTk.PhotoImage(imagem)
            label_imagem = tk.Label(frame_up, image=imagem_tk, bg="white")
            label_imagem.image = imagem_tk
            label_imagem.pack(expand=True)
        except Exception as e:
            tk.Label(frame_up, text=f"Erro ao carregar imagem: {e}", bg="white").pack(pady=20)
    else:
        tk.Label(frame_up, text="Imagem 'logo2.png' não encontrada.\nColoque ao lado do arquivo login_window.py", bg="white").pack(pady=20)

    # Botão de novo resgate
    tk.Button(root, text="Novo Resgate", command=lambda: nova_janela_resgate(root, usuario), bg="white", fg="#0B2B26").pack(pady=5)

    # Filtros
    filtro_frame = tk.Frame(root, bg="#0B2B26")
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Tipo:", bg="#0B2B26", fg="white").grid(row=0, column=0)
    filtro_tipo = tk.Entry(filtro_frame)
    filtro_tipo.grid(row=0, column=1, padx=5)

    tk.Label(filtro_frame, text="Localização:", bg="#0B2B26", fg="white").grid(row=0, column=2)
    filtro_localizacao = tk.Entry(filtro_frame)
    filtro_localizacao.grid(row=0, column=3, padx=5)

    tk.Label(filtro_frame, text="Responsável:", bg="#0B2B26", fg="white").grid(row=0, column=4)
    filtro_resp = tk.Entry(filtro_frame)
    filtro_resp.grid(row=0, column=5, padx=5)

    # Frame para dar borda visível na Treeview
    frame_tree = tk.Frame(root, bg="black", bd=1)
    frame_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    cols = ("id", "tipo", "data", "hora", "localizacao", "responsavel", "condicao", "observacoes")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings", height=8)

    # Estilo para Treeview com fundo #DAF1DE e texto centralizado
    style = ttk.Style()
    style.configure("Treeview",
                    background="#DAF1DE",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#DAF1DE")
    style.map('Treeview', background=[('selected', '#347083')])

    for col in cols:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")  # centraliza o conteúdo das colunas
        tree.column("id", width=50)
        tree.column("tipo", width=100)
        tree.column("data", width=90)
        tree.column("hora", width=70)
        tree.column("localizacao", width=140)
        tree.column("responsavel", width=130)
        tree.column("condicao", width=100)
        tree.column("observacoes", width=180)

    tree.pack(fill=tk.BOTH, expand=True)

    def carregar(filtrar=False):
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        query = "SELECT id, tipo, data, hora, localizacao, responsavel, condicao, observacoes FROM resgates WHERE usuario_id=?"
        params = [usuario[0]]

        if filtrar:
            if filtro_tipo.get():
                query += " AND tipo LIKE ?"
                params.append(f"%{filtro_tipo.get()}%")
            if filtro_localizacao.get():
                query += " AND localizacao LIKE ?"
                params.append(f"%{filtro_localizacao.get()}%")
            if filtro_resp.get():
                query += " AND responsavel LIKE ?"
                params.append(f"%{filtro_resp.get()}%")

        cursor.execute(query, params)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def excluir():
        selected = tree.selection()
        if not selected:
            return
        resgate_id = tree.item(selected[0])["values"][0]
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resgates WHERE id=?", (resgate_id,))
        conn.commit()
        conn.close()
        carregar()

    def editar():
        selected = tree.selection()
        if not selected:
            return
        dados = tree.item(selected[0])["values"]
        nova_janela_resgate(root, usuario, dados)
        carregar()

    def exportar_pdf():
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not path:
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Resgates de Animais", ln=True, align="C")
        pdf.ln(5)

        for item in tree.get_children():
            linha = tree.item(item)["values"]
            texto = f"ID: {linha[0]} | Tipo: {linha[1]} | Data: {linha[2]} {linha[3]} | Local: {linha[4]} | Resp: {linha[5]}\nCondição: {linha[6]} | Obs: {linha[7]}"
            pdf.multi_cell(0, 8, texto)
            pdf.ln(2)

        pdf.output(path)
        messagebox.showinfo("Exportação", "PDF exportado com sucesso.")

    def mostrar_grafico():
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT localizacao, COUNT(*) as total
            FROM resgates
            WHERE usuario_id=?
            GROUP BY localizacao
        ''', (usuario[0],))
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            messagebox.showinfo("Gráfico", "Nenhum dado para mostrar no gráfico.")
            return

        locais = [row[0] for row in resultados]
        quantidades = [row[1] for row in resultados]

        plt.figure(figsize=(10, 6))
        plt.bar(locais, quantidades, color="#0B2B26")
        plt.xlabel("Localização")
        plt.ylabel("Quantidade de Casos")
        plt.title("Quantidade de Casos por Localização")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
    # Botões
    frame_btns = tk.Frame(root, bg="#0B2B26")
    frame_btns.pack(pady=10)

    botoes = [
        ("Editar", editar),
        ("Excluir", excluir),
        ("Recarregar", carregar),
        ("Aplicar Filtros", lambda: carregar(filtrar=True)),
        ("Exportar PDF", exportar_pdf),
        ("Mostrar Gráfico", mostrar_grafico),
        ("Sair", root.destroy)
    ]

    for texto, comando in botoes:
        tk.Button(frame_btns, text=texto, command=comando, bg="white", fg="#0B2B26").pack(side=tk.LEFT, padx=5)

    carregar()
    root.mainloop()


def nova_janela_resgate(root, usuario, dados=None):
    win = tk.Toplevel(root)
    win.title("Novo Resgate" if dados is None else "Editar Resgate")
    win.configure(bg="#E3EDE6")
    win.geometry("600x500")

    labels = ["Tipo", "Data", "Hora (HH:MM)", "Localização", "Responsável", "Condição", "Observações"]
    entradas = []

    fonte = ("Arial", 11)

    for i, label in enumerate(labels):
        tk.Label(win, text=label, bg="#E3EDE6", font=fonte).grid(row=i, column=0, padx=10, pady=8, sticky="e")
        entry = tk.Entry(win, width=45, font=fonte, bg="#E3EDE6", highlightthickness=1, highlightbackground="#999", relief="flat")
        entry.grid(row=i, column=1, padx=10, pady=8)
        entradas.append(entry)

    if dados:
        for i in range(1, 8):  # ignora ID (posição 0)
            entradas[i - 1].insert(0, dados[i])

    def salvar():
        valores = [e.get() for e in entradas]
        if not all(valores[:6]):
            messagebox.showerror("Erro", "Campos obrigatórios não preenchidos.")
            return

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        if dados:
            cursor.execute('''
                UPDATE resgates SET tipo=?, data=?, hora=?, localizacao=?, responsavel=?, condicao=?, observacoes=?
                WHERE id=?
            ''', (*valores, dados[0]))
        else:
            cursor.execute('''
                INSERT INTO resgates (tipo, data, hora, localizacao, responsavel, condicao, observacoes, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*valores, usuario[0]))
        conn.commit()
        conn.close()
        win.destroy()

    btn_salvar = tk.Button(win, text="Salvar", command=salvar, font=fonte, bg="#0B2B26", fg="white", relief="flat", padx=10, pady=5)
    btn_salvar.grid(row=len(labels), column=1, pady=20)

