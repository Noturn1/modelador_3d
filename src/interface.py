import random
import tkinter as tk
from tkinter import colorchooser, messagebox
from logica import Cena

class InterfaceModelador:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelador 3D - Pipeline Alvy-Ray-Smith")

        # Configuração do Canvas
        self.largura = 1280
        self.altura = 720
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(False, False)

        self.cena = Cena(self.largura, self.altura)
        self.cena.definir_camera([0,0,100])

        self.painel_principal = tk.Frame(root)
        self.painel_principal.pack(fill=tk.BOTH, expand=True)

        self.painel_controles = tk.Frame(
            self.painel_principal, 
            width=280, 
            bg="lightgray"
        )

        self.painel_controles.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            self.painel_principal, 
            width= 1000, 
            height= 700, 
            bg="white"
        )

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Painel de Controles

        self._criar_painel_controles()

    def _criar_painel_controles(self):
        """
        Função que defini o painel com os controles da interface.
        """
        titulo = tk.Label(
            self.painel_controles, 
            text="Controles do Modelador 3D", 
            bg="gray",
            fg="white",
            font=("Arial", 14, "bold")
        )
        titulo.pack()

        btn_add_cubo = tk.Button(
            self.painel_controles, 
            text="Adicionar Cubo", 
            command=self.adicionar_cubo
        )
        btn_add_cubo.pack(pady=5)
        
        frame_coords = tk.Frame(self.painel_controles, bg="lightgray")
        frame_coords.pack(pady=10)

        tk.Label(frame_coords, text="X:", bg="lightgray").grid(row=0, column=0, padx=4)
        self.entry_x = tk.Entry(frame_coords, width=6)
        self.entry_x.grid(row=0, column=1)

        tk.Label(frame_coords, text="Y:", bg="lightgray").grid(row=0, column=2, padx=4)
        self.entry_y = tk.Entry(frame_coords, width=6)
        self.entry_y.grid(row=0, column=3)

        tk.Label(frame_coords, text="Z:", bg="lightgray").grid(row=0, column=4, padx=4)
        self.entry_z = tk.Entry(frame_coords, width=6)
        self.entry_z.grid(row=0, column=5)

        btn_add_luz = tk.Button(
            self.painel_controles,
            text="Adicionar Luz",
            command=lambda: self.adicionar_luz(
                self.entry_x.get(),
                self.entry_y.get(),
                self.entry_z.get()
            )
        )
        btn_add_luz.pack(pady=5)

        # ✅ Botão para limpar tela
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
    
    def adicionar_cubo(self):
        """
        Adiciona um cubo à cena.
        """
        self.cena.adicionar_objeto("OS CUBOS SERAO ADICIONADOS POR AQUI")

    def adicionar_luz(self, x, y, z):
        """
        Adiciona uma luz à cena.
        """
        print(x, y, z)
        self.cena.adicionar_luz("AS LUZES SERAO ADICIONADAS POR AQUI")

    def limpar_tela(self):
        """
        Remove todos os cubos do canvas.
        """

    def selecionar_objeto(self, event):
        pass
    
    def atualizar_cena(self):
        pass

    def renderizar_final(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceModelador(root)
    root.mainloop()
