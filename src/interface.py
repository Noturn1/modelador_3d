import random
import tkinter as tk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw
from .logica import Cena, Cubo, Luz, Mat4, Camera, Vector, Pipeline

class JanelaMateriais:
    """Janela flutuante para editar materiais do cubo"""
    def __init__(self, parent, callback, on_close=None):
        self.callback = callback
        self.on_close = on_close if on_close is not None else lambda: None
        self.janela = tk.Toplevel(parent)
        self.janela.title("Editar Materiais")
        self.janela.geometry("500x280")
        self.janela.resizable(False, False)
        self.janela.protocol("WM_DELETE_WINDOW", self._fechar)
        
        # Valores padrões
        self.ka_default = [0.2, 0.2, 0.2]
        self.kd_default = [0.8, 0.8, 0.8]
        self.ks_default = [1.0, 1.0, 1.0, 50]
        
        # Ambiente (Ka)
        tk.Label(self.janela, text="Ka (Ambiente) RGB:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        frame_ka = tk.Frame(self.janela)
        frame_ka.pack(padx=10, fill=tk.X)
        
        tk.Label(frame_ka, text="R:").pack(side=tk.LEFT, padx=2)
        self.entry_ka_r = tk.Scale(frame_ka, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ka_r.set(self.ka_default[0])
        self.entry_ka_r.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Label(frame_ka, text="G:").pack(side=tk.LEFT, padx=2)
        self.entry_ka_g = tk.Scale(frame_ka, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ka_g.set(self.ka_default[1])
        self.entry_ka_g.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Label(frame_ka, text="B:").pack(side=tk.LEFT, padx=2)
        self.entry_ka_b = tk.Scale(frame_ka, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ka_b.set(self.ka_default[2])
        self.entry_ka_b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Difuso (Kd)
        tk.Label(self.janela, text="Kd (Difuso) RGB:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        frame_kd = tk.Frame(self.janela)
        frame_kd.pack(padx=10, fill=tk.X)
        
        tk.Label(frame_kd, text="R:").pack(side=tk.LEFT, padx=2)
        self.entry_kd_r = tk.Scale(frame_kd, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_kd_r.set(self.kd_default[0])
        self.entry_kd_r.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Label(frame_kd, text="G:").pack(side=tk.LEFT, padx=2)
        self.entry_kd_g = tk.Scale(frame_kd, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_kd_g.set(self.kd_default[1])
        self.entry_kd_g.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Label(frame_kd, text="B:").pack(side=tk.LEFT, padx=2)
        self.entry_kd_b = tk.Scale(frame_kd, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_kd_b.set(self.kd_default[2])
        self.entry_kd_b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Especular (Ks)
        tk.Label(self.janela, text="Ks (Especular) RGB:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        frame_ks = tk.Frame(self.janela)
        frame_ks.pack(padx=10, fill=tk.X)
        
        tk.Label(frame_ks, text="R:").pack(side=tk.LEFT, padx=2)
        self.entry_ks_r = tk.Scale(frame_ks, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ks_r.set(self.ks_default[0])
        self.entry_ks_r.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Label(frame_ks, text="G:").pack(side=tk.LEFT, padx=2)
        self.entry_ks_g = tk.Scale(frame_ks, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ks_g.set(self.ks_default[1])
        self.entry_ks_g.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Label(frame_ks, text="B:").pack(side=tk.LEFT, padx=2)
        self.entry_ks_b = tk.Scale(frame_ks, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ks_b.set(self.ks_default[2])
        self.entry_ks_b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Botões
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)
        
        btn_ok = tk.Button(frame_botoes, text="OK", command=self.aplicar, width=10)
        btn_ok.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=self._fechar, width=10)
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def aplicar(self):
        """Retorna os valores modificados e fecha a janela"""
        materiais = {
            "ka": [self.entry_ka_r.get(), self.entry_ka_g.get(), self.entry_ka_b.get()],
            "kd": [self.entry_kd_r.get(), self.entry_kd_g.get(), self.entry_kd_b.get()],
            "ks": [self.entry_ks_r.get(), self.entry_ks_g.get(), self.entry_ks_b.get(), 50]
        }
        self.callback(materiais)
        self._fechar()

    def _fechar(self):
        if callable(self.on_close):
            self.on_close()
        self.janela.destroy()

class JanelaLuz:
    """Janela flutuante para editar intensidades de luz difusa e especular"""
    def __init__(self, parent, callback, tipo_inicial=Luz.DIRECIONAL, kd_inicial=None, ks_inicial=None, on_close=None):
        self.callback = callback
        self.on_close = on_close if on_close is not None else lambda: None
        self.janela = tk.Toplevel(parent)
        self.janela.title("Editar Intensidades da Luz")
        self.janela.geometry("500x280")
        self.janela.resizable(False, False)
        self.janela.protocol("WM_DELETE_WINDOW", self._fechar)

        self.kd_default = kd_inicial if kd_inicial is not None else [1.0, 1.0, 1.0]
        self.ks_default = ks_inicial if ks_inicial is not None else [1.0, 1.0, 1.0]

        # Difusa (Kd)
        tk.Label(self.janela, text="Intensidade Difusa (Kd) RGB:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        frame_kd = tk.Frame(self.janela)
        frame_kd.pack(padx=10, fill=tk.X)

        tk.Label(frame_kd, text="R:").pack(side=tk.LEFT, padx=2)
        self.entry_kd_r = tk.Scale(frame_kd, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_kd_r.set(self.kd_default[0])
        self.entry_kd_r.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Label(frame_kd, text="G:").pack(side=tk.LEFT, padx=2)
        self.entry_kd_g = tk.Scale(frame_kd, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_kd_g.set(self.kd_default[1])
        self.entry_kd_g.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Label(frame_kd, text="B:").pack(side=tk.LEFT, padx=2)
        self.entry_kd_b = tk.Scale(frame_kd, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_kd_b.set(self.kd_default[2])
        self.entry_kd_b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Especular (Ks)
        tk.Label(self.janela, text="Intensidade Especular (Ks) RGB:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        frame_ks = tk.Frame(self.janela)
        frame_ks.pack(padx=10, fill=tk.X)

        tk.Label(frame_ks, text="R:").pack(side=tk.LEFT, padx=2)
        self.entry_ks_r = tk.Scale(frame_ks, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ks_r.set(self.ks_default[0])
        self.entry_ks_r.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Label(frame_ks, text="G:").pack(side=tk.LEFT, padx=2)
        self.entry_ks_g = tk.Scale(frame_ks, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ks_g.set(self.ks_default[1])
        self.entry_ks_g.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        tk.Label(frame_ks, text="B:").pack(side=tk.LEFT, padx=2)
        self.entry_ks_b = tk.Scale(frame_ks, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.entry_ks_b.set(self.ks_default[2])
        self.entry_ks_b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.tipo_luz = tk.IntVar(value=tipo_inicial)
        tk.Label(self.janela, text="Tipo de Luz:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        frame_tipo_luz = tk.Frame(self.janela)
        frame_tipo_luz.pack(padx=10, fill=tk.X)

        tk.Radiobutton(frame_tipo_luz, text="Direcional", variable=self.tipo_luz, value=Luz.DIRECIONAL).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_tipo_luz, text="Pontual", variable=self.tipo_luz, value=Luz.PONTUAL).pack(side=tk.LEFT, padx=5)

        # Botões
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        btn_ok = tk.Button(frame_botoes, text="OK", command=self.aplicar, width=10)
        btn_ok.pack(side=tk.LEFT, padx=5)

        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=self._fechar, width=10)
        btn_cancelar.pack(side=tk.LEFT, padx=5)

    def aplicar(self):
        intensidades = {
            "tipo": self.tipo_luz.get(),
            "kd": [self.entry_kd_r.get(), self.entry_kd_g.get(), self.entry_kd_b.get()],
            "ks": [self.entry_ks_r.get(), self.entry_ks_g.get(), self.entry_ks_b.get()]
        }
        self.callback(intensidades)
        self._fechar()

    def _fechar(self):
        if callable(self.on_close):
            self.on_close()
        self.janela.destroy()

class InterfaceModelador:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelador 3D - Pipeline Alvy-Ray-Smith")

        # Configuração da Janela
        self.largura = 1000
        self.altura = 600
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(False, False)

        # Configuração do painel principal
        self.painel_principal = tk.Frame(root)
        self.painel_principal.pack(fill=tk.BOTH, expand=True)
        self.painel_controles = tk.Frame(
            self.painel_principal, 
            bg="lightgray"
        )

        # Criação do painel de controles
        self.painel_controles.pack(side=tk.RIGHT, fill=tk.Y)

        # Adicionando Canvas para painel principal
        self.canvas = tk.Canvas(
            self.painel_principal, 
            bg="white"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurando painel de controles
        self._criar_painel_controles()

        # Força UPDATE completo (não apenas idletasks)
        self.root.update()
        
        # Agora os tamanhos são reais
        largura_canvas = self.canvas.winfo_width()
        altura_canvas = self.canvas.winfo_height()

        print(f"Tamanho do canvas: {largura_canvas}x{altura_canvas}")
        
        # Fallback: se ainda estiver 1x1, calcula manualmente
        if largura_canvas <= 1 or altura_canvas <= 1:
            print("Fallback: canvas com tamanho inválido, calculando manualmente...")
            painel_controles_largura = self.painel_controles.winfo_width()
            if painel_controles_largura <= 1:
                painel_controles_largura = 200
            largura_canvas = self.largura - painel_controles_largura
            altura_canvas = self.altura
            print(f"Novo tamanho calculado: {largura_canvas}x{altura_canvas}")

        self.cena = Cena(
            altura_canvas,
            largura_canvas
        )

        self.camera = Camera(
            vrp=[30, 30, 30],
            prp=[0, 0, 0],
            vpn=[0, 0, 1],
            vup=[0, 1, 0],
            P=[0, 0, 0],
            Y=[0, 1, 0],
            u_min=-20, u_max=20, 
            v_min=-20, v_max=20, 
            DP=20,
            near=1, far=200,
            Vres=altura_canvas, Hres=largura_canvas
        )
        self.cena.definir_camera(self.camera)

        # Controle de seleção de cubos
        self.cubo_selecionado = None
        self.mostrar_grade = False  # Controle para exibir grade 3D
        
        # Materiais do cubo (padrões)
        self.materiais_cubo = {
            "ka": [0.2, 0.2, 0.2],
            "kd": [0.8, 0.8, 0.8],
            "ks": [1.0, 1.0, 1.0, 50]
        }
        self.intensidade_luz = {
            "kd": [1.0, 1.0, 1.0],
            "ks": [1.0, 1.0, 1.0]
        }
        self.tipo_luz = Luz.DIRECIONAL
        self.janela_materiais = None
        self.janela_luz = None

        self.root.after(0, self.atualizar_cena)

        print(self.painel_controles.winfo_width(), self.painel_controles.winfo_height())

    def _criar_painel_controles(self):
        """
        Função que define o painel com os controles da interface.
        """
        titulo = tk.Label(
            self.painel_controles, 
            text="Controles do Modelador 3D", 
            bg="gray",
            fg="white",
            font=("Arial", 14, "bold")
        )
        titulo.pack()

        frame_coords = tk.Frame(self.painel_controles, bg="lightgray")
        frame_coords.pack(pady=10)

        tk.Label(frame_coords, text="X:", bg="lightgray").grid(row=0, column=0, padx=4)
        self.entry_x = tk.Entry(frame_coords, width=6)
        self.entry_x.insert(0, "0")
        self.entry_x.grid(row=0, column=1)

        tk.Label(frame_coords, text="Y:", bg="lightgray").grid(row=0, column=2, padx=4)
        self.entry_y = tk.Entry(frame_coords, width=6)
        self.entry_y.insert(0, "0")
        self.entry_y.grid(row=0, column=3)

        tk.Label(frame_coords, text="Z:", bg="lightgray").grid(row=0, column=4, padx=4)
        self.entry_z = tk.Entry(frame_coords, width=6)
        self.entry_z.insert(0, "0")
        self.entry_z.grid(row=0, column=5)

        # Frame para botões de Adicionar Cubo e Editar Materiais
        frame_botoes_cubo = tk.Frame(self.painel_controles, bg="lightgray")
        frame_botoes_cubo.pack(pady=5)

        btn_add_cubo = tk.Button(
            frame_botoes_cubo, 
            text="Adicionar Cubo", 
            command=lambda: self.adicionar_cubo(
                int(self.entry_x.get()),
                int(self.entry_y.get()),
                int(self.entry_z.get())
            )
        )
        btn_add_cubo.pack(side=tk.LEFT, padx=3)

        btn_editar_materiais = tk.Button(
            frame_botoes_cubo,
            text="🎨",
            width=3,
            command=self.abrir_janela_materiais,
            font=("Arial", 12)
        )
        btn_editar_materiais.pack(side=tk.LEFT, padx=2)

        frame_botoes_luz = tk.Frame(self.painel_controles, bg="lightgray")
        frame_botoes_luz.pack(pady=5)

        btn_add_luz = tk.Button(
            frame_botoes_luz,
            text="Adicionar Luz",
            command=lambda: self.adicionar_luz(
                int(self.entry_x.get()),
                int(self.entry_y.get()),
                int(self.entry_z.get())
            )
        )
        btn_add_luz.pack(side=tk.LEFT, padx=3)

        btn_editar_luz = tk.Button(
            frame_botoes_luz,
            text="💡",
            width=3,
            command=self.abrir_janela_luz,
            font=("Arial", 12)
        )
        btn_editar_luz.pack(side=tk.LEFT, padx=2)

        btn_limpar = tk.Button(
            self.painel_controles,
            text="Limpar Tela",
            command=self.limpar_tela,
            bg="gray",
            fg="white",
            font=("Arial", 12),
            width=20
        )
        btn_limpar.pack(pady=5)

        # Lista de objetos da cena
        tk.Label(
            self.painel_controles,
            text="Objetos na Cena",
            bg="lightgray",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))
        
        self.lista_objetos = tk.Listbox(
            self.painel_controles,
            width=30,
            height=8
        )
        self.lista_objetos.pack(pady=5)
        self.lista_objetos.bind('<<ListboxSelect>>', self.selecionar_objeto_lista)

        # Controles de movimentação (cruz direcional)
        tk.Label(
            self.painel_controles,
            text="Mover Objeto",
            bg="lightgray",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))
        
        frame_movimento = tk.Frame(self.painel_controles, bg="lightgray")
        frame_movimento.pack(pady=5)
        
        # Botão Cima (↑)
        btn_cima = tk.Button(
            frame_movimento,
            text="▲",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.mover_objeto(dx=0, dy=5, dz=0)
        )
        btn_cima.grid(row=0, column=1, padx=2, pady=2)
        
        # Botão Esquerda (←)
        btn_esquerda = tk.Button(
            frame_movimento,
            text="◄",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.mover_objeto(dx=-5, dy=0, dz=0)
        )
        btn_esquerda.grid(row=1, column=0, padx=2, pady=2)
        
        # Botão Direita (→)
        btn_direita = tk.Button(
            frame_movimento,
            text="►",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.mover_objeto(dx=5, dy=0, dz=0)
        )
        btn_direita.grid(row=1, column=2, padx=2, pady=2)
        
        # Botão Baixo (▼)
        btn_baixo = tk.Button(
            frame_movimento,
            text="▼",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.mover_objeto(dx=0, dy=-5, dz=0)
        )
        btn_baixo.grid(row=2, column=1, padx=2, pady=2)

    
    def abrir_janela_materiais(self):
        """
        Abre a janela flutuante para editar materiais do cubo.
        """
        if self.janela_materiais is not None and self.janela_materiais.janela.winfo_exists():
            self.janela_materiais.janela.lift()
            self.janela_materiais.janela.focus_force()
            return
        self.janela_materiais = JanelaMateriais(
            self.root,
            self.aplicar_materiais,
            on_close=self._fechar_janela_materiais
        )

    def _fechar_janela_materiais(self):
        self.janela_materiais = None

    def abrir_janela_luz(self):
        """
        Abre a janela flutuante para editar intensidades da luz.
        """
        if self.janela_luz is not None and self.janela_luz.janela.winfo_exists():
            self.janela_luz.janela.lift()
            self.janela_luz.janela.focus_force()
            return
        self.janela_luz = JanelaLuz(
            self.root,
            self.aplicar_intensidades_luz,
            tipo_inicial=self.tipo_luz,
            ks_inicial=self.intensidade_luz["ks"],
            kd_inicial=self.intensidade_luz["kd"],
            on_close=self._fechar_janela_luz
        )

    def _fechar_janela_luz(self):
        self.janela_luz = None
    
    def aplicar_materiais(self, materiais):
        """
        Aplica os materiais modificados e armazena os valores.
        """
        self.materiais_cubo = materiais
        messagebox.showinfo("Sucesso", "Materiais atualizados! Próximo cubo usará essas cores.")

    def aplicar_intensidades_luz(self, intensidades):
        """
        Aplica as intensidades difusa e especular da luz.
        """
        self.tipo_luz = intensidades.get("tipo", self.tipo_luz)
        self.intensidade_luz = {
            "kd": intensidades["kd"],
            "ks": intensidades["ks"]
        }
        messagebox.showinfo("Sucesso", "Intensidades da luz atualizadas! Próxima luz usará esses valores.")

    def adicionar_cubo(self, x: int = 0, y: int = 0, z: int = 0):
        """
        Adiciona um cubo à cena com os materiais atualmente configurados.
        """
        cubo = Cubo(
            [x, y, z],
            20,
            ka=self.materiais_cubo["ka"],
            kd=self.materiais_cubo["kd"],
            ks=self.materiais_cubo["ks"]
        )
        self.cena.adicionar_objeto(cubo)
        centroide = cubo.centroide
        # Adicionar à lista visual
        num_cubo = len(self.cena.objetos)                  # Pos: ({x}, {y}, {z})")
        self.lista_objetos.insert(tk.END, f"Cubo {num_cubo} - Pos: ({centroide[0]}, {centroide[1]}, {centroide[2]})")
        
        self.atualizar_cena()

    def mover_objeto(self, dx, dy, dz):
        """
        Move o objeto selecionado na direção especificada.
        """
        if self.cubo_selecionado is None:
            messagebox.showwarning("Aviso", "Nenhum cubo selecionado!")
            return
        
        # Aplicar translação ao cubo selecionado
        mat_trans = Mat4.trans(dx, dy, dz)
        self.cubo_selecionado.aplicar_transformacao(mat_trans)
        
        self.atualizar_cena()

    def adicionar_luz(self, x: int = 0, y: int = 0, z: int = 0):
        """
        Adiciona uma luz à cena.
        """
        self.luz = Luz(
            self.tipo_luz,            # Tipo de luz
            [x, y, z],              # Intensidade ambiente RGB
            self.intensidade_luz["kd"],              # Intensidade difusa RGB
            self.intensidade_luz["ks"]               # Intensidade especular RGB
        )
        self.cena.adicionar_luz(self.luz)

        self.atualizar_cena()

    def limpar_tela(self):
        """
        Remove todos os cubos do canvas.
        """
        self.cena.objetos.clear()
        self.cena.luzes.clear()
        self.lista_objetos.delete(0, tk.END)
        self.cubo_selecionado = None
        self.atualizar_cena()

    def selecionar_objeto_lista(self, event):
        """
        Seleciona um cubo da lista para transformações.
        """
        selecionado = self.lista_objetos.curselection()
        if selecionado:
            idx = selecionado[0]
            if idx < len(self.cena.objetos):
                self.cubo_selecionado = self.cena.objetos[idx]
                print(f"Cubo {idx + 1} selecionado")

    def selecionar_objeto(self, event):
        pass

    def atualizar_cena(self):
        self.cena.renderizar()
        self._mostrar_cena_no_canvas()

    def renderizar_final(self):
        self.atualizar_cena()

    def _mostrar_cena_no_canvas(self):
        """
        Converte o color_buffer da cena e exibe no canvas.
        """
        largura = self.cena.width
        altura = self.cena.height

        # Diagnóstico rápido: contar pixels coloridos
        pixels_coloridos = 0
        for x in range(largura):
            for y in range(altura):
                cor = self.cena.color_buffer[x][y]
                if cor != (0, 0, 0) and cor != [0, 0, 0]:
                    pixels_coloridos += 1
                    break
            if pixels_coloridos:
                break

        # Criar imagem PIL a partir do color_buffer
        img = Image.new("RGB", (largura, altura))
        pixels = img.load()
        for x in range(largura):
            for y in range(altura):
                cor = self.cena.color_buffer[x][y]
                r, g, b = (int(c) for c in cor)
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                pixels[x, y] = (r, g, b)

        self._imagem_canvas = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self._imagem_canvas)
        
        # Desenhar grade 3D por cima da cena renderizada
        if self.mostrar_grade:
            self._desenhar_grade_3d()

    def _desenhar_grade_3d(self):
        """
        Desenha uma grade 3D no canvas usando as projeções da câmera.
        """
        # Criar linhas da grade no espaço 3D
        tamanho_grade = 40
        espacamento = 5
        
        # Obter matrizes de projeção
        mat_A = Pipeline.get_matrix_A(self.camera.vrp)
        mat_B = Pipeline.get_matrix_B(self.camera.u, self.camera.v, self.camera.n)
        mat_C = Pipeline.get_matrix_C(self.camera.Cu, self.camera.Cv, self.camera.DP)
        mat_D = Pipeline.get_matrix_D(
            self.camera.Su, self.camera.Sv, self.camera.DP, self.camera.far
        )
        mat_P = Pipeline.get_matrix_P(self.camera.far, self.camera.near)
        
        mat_J = Pipeline.get_matrix_J()
        mat_K = Pipeline.get_matrix_K()
        mat_L = Pipeline.get_matrix_L(
            self.cena.viewport["x_max"],
            self.cena.viewport["x_min"],
            self.cena.viewport["y_max"],
            self.cena.viewport["y_min"],
            self.camera.z_max,
            self.camera.z_min,
        )
        mat_M = Pipeline.get_matrix_M()
        
        m_view = Mat4.mul(mat_B, mat_A)
        m_proj = Mat4.mul(mat_P, Mat4.mul(mat_D, mat_C))
        m_total_proj = Mat4.mul(m_proj, m_view)
        m_screen = Mat4.mul(mat_M, Mat4.mul(mat_L, Mat4.mul(mat_K, mat_J)))
        
        def projetar_ponto(x, y, z):
            """Projeta um ponto 3D para coordenadas de tela com validação"""
            try:
                v_mundo = [x, y, z, 1.0]
                v_clip = Vector.mul(m_total_proj, v_mundo)
                w = v_clip[3]
                
                # Verificar se o ponto está muito próximo ou atrás da câmera
                if abs(w) < 0.001:
                    return None
                
                v_ndc = [v_clip[0] / w, v_clip[1] / w, v_clip[2] / w, 1.0]
                
                # Verificar se está dentro do volume de visualização
                if abs(v_ndc[0]) > 2 or abs(v_ndc[1]) > 2 or v_ndc[2] < 0 or v_ndc[2] > 1:
                    return None
                
                v_tela = Vector.mul(m_screen, v_ndc)
                px, py = int(v_tela[0]), int(v_tela[1])
                
                # Validar limites da tela
                if px < -1000 or px > self.cena.width + 1000 or py < -1000 or py > self.cena.height + 1000:
                    return None
                
                return px, py
            except:
                return None
        
        # Desenhar linhas paralelas ao eixo X (no plano Y=0)
        for z in range(-tamanho_grade, tamanho_grade + 1, espacamento):
            p1 = projetar_ponto(-tamanho_grade, 0, z)
            p2 = projetar_ponto(tamanho_grade, 0, z)
            
            if p1 and p2:
                cor = "red" if z == 0 else "#ff9999"
                largura = 2 if z == 0 else 1
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                       fill=cor, width=largura, 
                                       dash=() if z == 0 else (3, 3))
        
        # Desenhar linhas paralelas ao eixo Z (no plano Y=0)
        for x in range(-tamanho_grade, tamanho_grade + 1, espacamento):
            p1 = projetar_ponto(x, 0, -tamanho_grade)
            p2 = projetar_ponto(x, 0, tamanho_grade)
            
            if p1 and p2:
                cor = "blue" if x == 0 else "#9999ff"
                largura = 2 if x == 0 else 1
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                       fill=cor, width=largura, 
                                       dash=() if x == 0 else (3, 3))
        
        # Desenhar eixos principais 3D com setas
        # Eixo X (vermelho)
        p1 = projetar_ponto(-tamanho_grade, 0, 0)
        p2 = projetar_ponto(tamanho_grade, 0, 0)
        if p1 and p2:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                   fill="red", width=2, arrow=tk.LAST)
        
        # Eixo Y (verde)
        p1 = projetar_ponto(0, -tamanho_grade, 0)
        p2 = projetar_ponto(0, tamanho_grade, 0)
        if p1 and p2:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                   fill="green", width=2, arrow=tk.LAST)
        
        # Eixo Z (azul)
        p1 = projetar_ponto(0, 0, -tamanho_grade)
        p2 = projetar_ponto(0, 0, tamanho_grade)
        if p1 and p2:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                   fill="blue", width=2, arrow=tk.LAST)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceModelador(root)
    root.mainloop()