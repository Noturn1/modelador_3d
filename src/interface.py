import random
import tkinter as tk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw
from .logica import Cena, Cubo, Luz, Mat4, Camera, Vector, Pipeline

class JanelaMateriais:
    """Janela flutuante para editar materiais do cubo"""
    # ALTERAÇÃO 1: Adicionado parametro materiais_iniciais=None
    def __init__(self, parent, callback, on_close=None, materiais_iniciais=None):
        self.callback = callback
        self.on_close = on_close if on_close is not None else lambda: None
        self.janela = tk.Toplevel(parent)
        self.janela.title("Editar Materiais")
        self.janela.geometry("500x280")
        self.janela.resizable(False, False)
        self.janela.protocol("WM_DELETE_WINDOW", self._fechar)
        
        # Valores padrões ou herdados do cubo selecionado
        if materiais_iniciais:
            self.ka_default = materiais_iniciais['ka']
            self.kd_default = materiais_iniciais['kd']
            self.ks_default = materiais_iniciais['ks']
        else:
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
        self.largura = 1200
        self.altura = 600
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(False, False)

        # Configuração do painel principal
        self.painel_principal = tk.Frame(root)
        self.painel_principal.pack(fill=tk.BOTH, expand=True)
        # Painel de controles com rolagem
        self.frame_controles_wrapper = tk.Frame(self.painel_principal, bg="lightgray")
        self.frame_controles_wrapper.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_controles = tk.Canvas(
            self.frame_controles_wrapper,
            bg="lightgray",
            highlightthickness=0,
            width=360
        )
        self.scrollbar_controles = tk.Scrollbar(
            self.frame_controles_wrapper,
            orient=tk.VERTICAL,
            command=self.canvas_controles.yview
        )

        self.painel_controles = tk.Frame(
            self.canvas_controles,
            bg="lightgray"
        )

        self.painel_controles.bind(
            "<Configure>",
            lambda e: self.canvas_controles.configure(scrollregion=self.canvas_controles.bbox("all"))
        )

        self.canvas_controles.create_window((0, 0), window=self.painel_controles, anchor="nw")
        self.canvas_controles.configure(yscrollcommand=self.scrollbar_controles.set)

        def _on_mousewheel(event):
            self.canvas_controles.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas_controles.bind_all("<MouseWheel>", _on_mousewheel)

        self.canvas_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_controles.pack(side=tk.RIGHT, fill=tk.Y)

        # Adicionando Canvas para painel principal
        self.canvas = tk.Canvas(
            self.painel_principal, 
            bg="white"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.camera_config = {
            "vrp": [0, 0, 40],
            "prp": [0, 0, 0],
            "vpn": [0, 0, 1],
            "vup": [0, 1, 0],
            "P": [0, 0, 0],
            "Y": [0, 1, 0],
            "u_min": -141, "u_max": 141,
            "v_min": -100, "v_max": 100,
            "DP": 100,
            "near": 1, "far": 200,
        }

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
            vrp=self.camera_config["vrp"],
            prp=self.camera_config["prp"],
            vpn=self.camera_config["vpn"],
            vup=self.camera_config["vup"],
            P=self.camera_config["P"],
            Y=self.camera_config["Y"],
            # proporção da tela 1.415:1
            u_min=self.camera_config["u_min"], u_max=self.camera_config["u_max"], 
            v_min=self.camera_config["v_min"], v_max=self.camera_config["v_max"], 
            DP=self.camera_config["DP"],
            near=self.camera_config["near"], far=self.camera_config["far"],
            Vres=altura_canvas, Hres=largura_canvas
        )
        self.cena.definir_camera(self.camera)

        # Controle de seleção de cubos
        self.cubo_selecionado = None
        self.mostrar_grade = False  # Controle para exibir grade 3D
        self.modo_shader = 2  # 1 = Flat, 2 = Phong
        
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

        self.root.bind("<Up>", lambda event: self.mover_objeto(dx=0, dy=5, dz=0))
        self.root.bind("<Down>", lambda event: self.mover_objeto(dx=0, dy=-5, dz=0))
        self.root.bind("<Left>", lambda event: self.mover_objeto(dx=-5, dy=0, dz=0))
        self.root.bind("<Right>", lambda event: self.mover_objeto(dx=5, dy=0, dz=0))
        self.root.bind("<Shift-Up>", lambda event: self.mover_objeto(dx=0, dy=0, dz=-5))
        self.root.bind("<Shift-Down>", lambda event: self.mover_objeto(dx=0, dy=0, dz=5))
        self.root.bind("<d>", lambda event: self.rotacionar_objeto(eixo='y', tetha=5))
        self.root.bind("<a>", lambda event: self.rotacionar_objeto(eixo='y', tetha=-5))
        self.root.bind("<s>", lambda event: self.rotacionar_objeto(eixo='x', tetha=5))
        self.root.bind("<w>", lambda event: self.rotacionar_objeto(eixo='x', tetha=-5))
        self.root.bind("<q>", lambda event: self.rotacionar_objeto(eixo='z', tetha=5))
        self.root.bind("<e>", lambda event: self.rotacionar_objeto(eixo='z', tetha=-5))


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

        # ALTERAÇÃO 2: Novo botão logo abaixo do frame de luzes
        btn_edit_mat_cubo = tk.Button(
            self.painel_controles,
            text="Editar Cubo Selecionado",
            command=self.abrir_edicao_cubo_selecionado,
            bg="lightgray"
        )
        btn_edit_mat_cubo.pack(pady=5)

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
        self.lista_objetos.bind("<FocusIn>", lambda event: self.root.focus())

        # Controles de escala (X, Y, Z)
        tk.Label(
            self.painel_controles,
            text="Escalar Objeto",
            bg="lightgray",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))
        
        frame_escala = tk.Frame(self.painel_controles, bg="lightgray")
        frame_escala.pack(pady=5)

        tk.Label(frame_escala, text="X", bg="lightgray", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6)
        tk.Label(frame_escala, text="Y", bg="lightgray", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=6)
        tk.Label(frame_escala, text="Z", bg="lightgray", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=6)

        btn_x_mais = tk.Button(
            frame_escala,
            text="+",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.escala_objeto(1.1, 1.0, 1.0)
        )
        btn_x_mais.grid(row=1, column=0, padx=4, pady=2)

        btn_y_mais = tk.Button(
            frame_escala,
            text="+",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.escala_objeto(1.0, 1.1, 1.0)
        )
        btn_y_mais.grid(row=1, column=1, padx=4, pady=2)

        btn_z_mais = tk.Button(
            frame_escala,
            text="+",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.escala_objeto(1.0, 1.0, 1.1)
        )
        btn_z_mais.grid(row=1, column=2, padx=4, pady=2)

        btn_x_menos = tk.Button(
            frame_escala,
            text="-",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.escala_objeto(0.9, 1.0, 1.0)
        )
        btn_x_menos.grid(row=2, column=0, padx=4, pady=2)

        btn_y_menos = tk.Button(
            frame_escala,
            text="-",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.escala_objeto(1.0, 0.9, 1.0)
        )
        btn_y_menos.grid(row=2, column=1, padx=4, pady=2)

        btn_z_menos = tk.Button(
            frame_escala,
            text="-",
            width=4,
            height=2,
            font=("Arial", 14),
            command=lambda: self.escala_objeto(1.0, 1.0, 0.9)
        )
        btn_z_menos.grid(row=2, column=2, padx=4, pady=2)

        # Parâmetros da câmera
        tk.Label(
            self.painel_controles,
            text="Parâmetros da Câmera",
            bg="lightgray",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))

        frame_camera = tk.Frame(self.painel_controles, bg="lightgray")
        frame_camera.pack(pady=5)

        def _fmt_vec(v):
            return f"{v[0]}, {v[1]}, {v[2]}"

        tk.Label(frame_camera, text="VRP", bg="lightgray").grid(row=0, column=0, sticky="e", padx=4, pady=2)
        self.entry_vrp = tk.Entry(frame_camera, width=18)
        self.entry_vrp.insert(0, _fmt_vec(self.camera_config["vrp"]))
        self.entry_vrp.grid(row=0, column=1, padx=4, pady=2)

        tk.Label(frame_camera, text="PRP", bg="lightgray").grid(row=1, column=0, sticky="e", padx=4, pady=2)
        self.entry_prp = tk.Entry(frame_camera, width=18)
        self.entry_prp.insert(0, _fmt_vec(self.camera_config["prp"]))
        self.entry_prp.grid(row=1, column=1, padx=4, pady=2)

        tk.Label(frame_camera, text="VPN", bg="lightgray").grid(row=2, column=0, sticky="e", padx=4, pady=2)
        self.entry_vpn = tk.Entry(frame_camera, width=18)
        self.entry_vpn.insert(0, _fmt_vec(self.camera_config["vpn"]))
        self.entry_vpn.grid(row=2, column=1, padx=4, pady=2)

        tk.Label(frame_camera, text="VUP", bg="lightgray").grid(row=3, column=0, sticky="e", padx=4, pady=2)
        self.entry_vup = tk.Entry(frame_camera, width=18)
        self.entry_vup.insert(0, _fmt_vec(self.camera_config["vup"]))
        self.entry_vup.grid(row=3, column=1, padx=4, pady=2)

        tk.Label(frame_camera, text="P", bg="lightgray").grid(row=4, column=0, sticky="e", padx=4, pady=2)
        self.entry_p = tk.Entry(frame_camera, width=18)
        self.entry_p.insert(0, _fmt_vec(self.camera_config["P"]))
        self.entry_p.grid(row=4, column=1, padx=4, pady=2)

        tk.Label(frame_camera, text="Y", bg="lightgray").grid(row=5, column=0, sticky="e", padx=4, pady=2)
        self.entry_y_cam = tk.Entry(frame_camera, width=18)
        self.entry_y_cam.insert(0, _fmt_vec(self.camera_config["Y"]))
        self.entry_y_cam.grid(row=5, column=1, padx=4, pady=2)

        tk.Label(frame_camera, text="u_min", bg="lightgray").grid(row=6, column=0, sticky="e", padx=4, pady=2)
        self.entry_u_min = tk.Entry(frame_camera, width=8)
        self.entry_u_min.insert(0, str(self.camera_config["u_min"]))
        self.entry_u_min.grid(row=6, column=1, sticky="w", padx=(4, 8), pady=2)

        tk.Label(frame_camera, text="u_max", bg="lightgray").grid(row=6, column=2, sticky="e", padx=4, pady=2)
        self.entry_u_max = tk.Entry(frame_camera, width=8)
        self.entry_u_max.insert(0, str(self.camera_config["u_max"]))
        self.entry_u_max.grid(row=6, column=3, sticky="w", padx=(4, 2), pady=2)

        tk.Label(frame_camera, text="v_min", bg="lightgray").grid(row=7, column=0, sticky="e", padx=4, pady=2)
        self.entry_v_min = tk.Entry(frame_camera, width=8)
        self.entry_v_min.insert(0, str(self.camera_config["v_min"]))
        self.entry_v_min.grid(row=7, column=1, sticky="w", padx=(4, 8), pady=2)

        tk.Label(frame_camera, text="v_max", bg="lightgray").grid(row=7, column=2, sticky="e", padx=4, pady=2)
        self.entry_v_max = tk.Entry(frame_camera, width=8)
        self.entry_v_max.insert(0, str(self.camera_config["v_max"]))
        self.entry_v_max.grid(row=7, column=3, sticky="w", padx=(4, 2), pady=2)

        tk.Label(frame_camera, text="DP", bg="lightgray").grid(row=8, column=0, sticky="e", padx=4, pady=2)
        self.entry_dp = tk.Entry(frame_camera, width=8)
        self.entry_dp.insert(0, str(self.camera_config["DP"]))
        self.entry_dp.grid(row=8, column=1, sticky="w", padx=(4, 8), pady=2)

        tk.Label(frame_camera, text="near", bg="lightgray").grid(row=8, column=2, sticky="e", padx=4, pady=2)
        self.entry_near = tk.Entry(frame_camera, width=8)
        self.entry_near.insert(0, str(self.camera_config["near"]))
        self.entry_near.grid(row=8, column=3, sticky="w", padx=(4, 2), pady=2)

        tk.Label(frame_camera, text="far", bg="lightgray").grid(row=9, column=0, sticky="e", padx=4, pady=2)
        self.entry_far = tk.Entry(frame_camera, width=8)
        self.entry_far.insert(0, str(self.camera_config["far"]))
        self.entry_far.grid(row=9, column=1, sticky="w", padx=(4, 2), pady=2)

        btn_aplicar_camera = tk.Button(
            self.painel_controles,
            text="Aplicar Câmera",
            command=self.aplicar_parametros_camera,
            bg="gray",
            fg="white",
            font=("Arial", 11),
            width=20
        )
        btn_aplicar_camera.pack(pady=(5, 10))

        # Seletor de modo de iluminação
        tk.Label(
            self.painel_controles,
            text="Modo de Iluminação",
            bg="lightgray",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))

        frame_shader = tk.Frame(self.painel_controles, bg="lightgray")
        frame_shader.pack(pady=5)

        self.shader_var = tk.IntVar(value=2)  # 1=Flat, 2=Phong

        tk.Radiobutton(
            frame_shader,
            text="Flat",
            variable=self.shader_var,
            value=1,
            bg="lightgray",
            command=self.alterar_modo_iluminacao
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            frame_shader,
            text="Phong",
            variable=self.shader_var,
            value=2,
            bg="lightgray",
            command=self.alterar_modo_iluminacao
        ).pack(side=tk.LEFT, padx=10)
    
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

    # ALTERAÇÃO 3: Métodos para abrir janela de edição e aplicar mudanças
    def abrir_edicao_cubo_selecionado(self):
        if not self.cubo_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cubo na lista primeiro!")
            return
        
        # Prepara os valores atuais do cubo
        mat_atuais = {
            "ka": self.cubo_selecionado.ka,
            "kd": self.cubo_selecionado.kd,
            "ks": self.cubo_selecionado.ks
        }
        
        # Abre a janela passando os materiais atuais e o callback específico
        JanelaMateriais(
            self.root, 
            self.aplicar_edicao_cubo, 
            materiais_iniciais=mat_atuais
        )

    def aplicar_edicao_cubo(self, materiais):
        if self.cubo_selecionado:
            self.cubo_selecionado.ka = materiais["ka"]
            self.cubo_selecionado.kd = materiais["kd"]
            # ks vem com 4 valores (incluindo o expoente 50), o cubo aceita
            self.cubo_selecionado.ks = materiais["ks"]
            
            self.atualizar_cena()
            messagebox.showinfo("Sucesso", "Material do cubo atualizado!")

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
        
        self.atualizar_lista_objetos()
        self.atualizar_cena()

    def atualizar_lista_objetos(self):
        """
        Atualiza a lista de objetos com as posições atualizadas dos centroides.
        """
        self.lista_objetos.delete(0, tk.END)
        for i, obj in enumerate(self.cena.objetos):
            centroide = obj.centroide
            self.lista_objetos.insert(tk.END, f"Cubo {i+1} - Pos: ({centroide[0]:.1f}, {centroide[1]:.1f}, {centroide[2]:.1f})")

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
        
        self.atualizar_lista_objetos()
        self.atualizar_cena()

    def rotacionar_objeto(self, eixo, tetha):
        """
        Rotaciona o objeto selecionado em torno do eixo especificado.
        """
        if self.cubo_selecionado is None:
            messagebox.showwarning("Aviso", "Nenhum cubo selecionado!")
            return
        
        if eixo == 'x':
            mat_rot = Mat4.rotate_x(tetha=tetha, centroide=self.cubo_selecionado.centroide)
        elif eixo == 'y':
            mat_rot = Mat4.rotate_y(tetha=tetha, centroide=self.cubo_selecionado.centroide)
        elif eixo == 'z':
            mat_rot = Mat4.rotate_z(tetha=tetha, centroide=self.cubo_selecionado.centroide)
        else:
            messagebox.showerror("Erro", "Eixo inválido para rotação!")
            return
        
        self.cubo_selecionado.aplicar_transformacao(mat_rot)
        
        self.atualizar_lista_objetos()
        self.atualizar_cena()

    def escala_objeto(self, sx, sy, sz):
        """
        Escala o objeto selecionado pelos fatores especificados.
        """
        if self.cubo_selecionado is None:
            messagebox.showwarning("Aviso", "Nenhum cubo selecionado!")
            return
        
        mat_escala = Mat4.scale(sx, sy, sz, centroide=self.cubo_selecionado.centroide)
        self.cubo_selecionado.aplicar_transformacao(mat_escala)
        
        self.atualizar_lista_objetos()
        self.atualizar_cena()

    def alterar_modo_iluminacao(self):
        """
        Altera o modo de iluminação entre Flat e Phong.
        """
        self.modo_shader = self.shader_var.get()
        self.atualizar_cena()

    def _parse_vector_entry(self, entry, nome):
        texto = entry.get().strip()
        partes = [p.strip() for p in texto.split(",") if p.strip() != ""]
        if len(partes) != 3:
            raise ValueError(f"{nome} deve ter 3 valores (ex: 0, 0, 40)")
        return [float(partes[0]), float(partes[1]), float(partes[2])]

    def aplicar_parametros_camera(self):
        """
        Aplica os parâmetros da câmera informados nos campos.
        """
        try:
            vrp = self._parse_vector_entry(self.entry_vrp, "VRP")
            prp = self._parse_vector_entry(self.entry_prp, "PRP")
            vpn = self._parse_vector_entry(self.entry_vpn, "VPN")
            vup = self._parse_vector_entry(self.entry_vup, "VUP")
            p = self._parse_vector_entry(self.entry_p, "P")
            y = self._parse_vector_entry(self.entry_y_cam, "Y")

            u_min = float(self.entry_u_min.get())
            u_max = float(self.entry_u_max.get())
            v_min = float(self.entry_v_min.get())
            v_max = float(self.entry_v_max.get())
            dp = float(self.entry_dp.get())
            near = float(self.entry_near.get())
            far = float(self.entry_far.get())

            if near <= 0 or far <= 0 or near >= far:
                messagebox.showerror("Erro", "Parâmetros inválidos: near deve ser menor que far e ambos > 0.")
                return

            self.camera_config = {
                "vrp": vrp,
                "prp": prp,
                "vpn": vpn,
                "vup": vup,
                "P": p,
                "Y": y,
                "u_min": u_min,
                "u_max": u_max,
                "v_min": v_min,
                "v_max": v_max,
                "DP": dp,
                "near": near,
                "far": far,
            }
            self.camera = Camera(
                vrp=self.camera_config["vrp"],
                prp=self.camera_config["prp"],
                vpn=self.camera_config["vpn"],
                vup=self.camera_config["vup"],
                P=self.camera_config["P"],
                Y=self.camera_config["Y"],
                u_max=self.camera_config["u_max"],
                u_min=self.camera_config["u_min"],
                v_max=self.camera_config["v_max"],
                v_min=self.camera_config["v_min"],
                DP=self.camera_config["DP"],
                near=self.camera_config["near"],
                far=self.camera_config["far"],
                Vres=self.camera.Vres,
                Hres=self.camera.Hres,
            )
            self.cena.definir_camera(self.camera)
            self.atualizar_cena()
        except ValueError as exc:
            messagebox.showerror("Erro", f"Valores inválidos: {exc}")

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
        self.cena.modo_shader = self.modo_shader
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

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceModelador(root)
    root.mainloop()