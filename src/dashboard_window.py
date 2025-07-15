# dashboard_window.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from fpdf import FPDF

def abrir_dashboard(usuario):
    root = tk.Tk()
    root.title("Sistema de Resgates de Animais")

    tk.Label(root, text=f"Usuário logado: {usuario[1]} ({usuario[2]})", fg="green").pack(pady=5)
    tk.Button(root, text="Novo Resgate", command=lambda: nova_janela_resgate(root, usuario)).pack()

    # Filtros
    filtro_frame = tk.Frame(root)
    filtro_frame.pack()

    tk.Label(filtro_frame, text="Tipo:").grid(row=0, column=0)
    filtro_tipo = tk.Entry(filtro_frame)
    filtro_tipo.grid(row=0, column=1)

    tk.Label(filtro_frame, text="Data (AAAA-MM-DD):").grid(row=0, column=2)
    filtro_data = tk.Entry(filtro_frame)
    filtro_data.grid(row=0, column=3)

    tk.Label(filtro_frame, text="Responsável:").grid(row=0, column=4)
    filtro_resp = tk.Entry(filtro_frame)
    filtro_resp.grid(row=0, column=5)

    # Tabela de resgates
    cols = ("id", "tipo", "data", "hora", "localizacao", "responsavel", "condicao", "observacoes")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=12)
    for col in cols:
        tree.heading(col, text=col.capitalize())
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

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
            if filtro_data.get():
                query += " AND data=?"
                params.append(filtro_data.get())
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

    # Botões
    frame_btns = tk.Frame(root)
    frame_btns.pack()
    tk.Button(frame_btns, text="Editar", command=editar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btns, text="Excluir", command=excluir).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btns, text="Recarregar", command=carregar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btns, text="Aplicar Filtros", command=lambda: carregar(filtrar=True)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btns, text="Exportar PDF", command=exportar_pdf).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btns, text="Sair", command=root.destroy).pack(side=tk.LEFT, padx=5)

    carregar()
    root.mainloop()

def nova_janela_resgate(root, usuario, dados=None):
    win = tk.Toplevel(root)
    win.title("Novo Resgate" if dados is None else "Editar Resgate")

    labels = ["Tipo", "Data (AAAA-MM-DD)", "Hora (HH:MM)", "Localização", "Responsável", "Condição", "Observações"]
    entradas = []

    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entry = tk.Entry(win, width=50)
        entry.grid(row=i, column=1)
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

    tk.Button(win, text="Salvar", command=salvar).grid(row=len(labels), column=1)
