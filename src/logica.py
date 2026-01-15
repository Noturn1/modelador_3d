import math

class Mat4:

    def identity(self):
        return(
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        )


class Face:
    # define a face do objeto, vertices são tuplas (x,y,z)

    def __init__(self, v0, v2, v3, v4):
        self.lista_vertices = (v0, v2, v3, v4) # Usar tupla pq tem tamanho fixo
        self.normal = self.calcular_normal(self) # Se usar lista, um .append() pode mudar o tamanho
        

    def calcular_normal(self):
        A, B, C = self.vertices[0], self.vertices[1], self.vertices[3]
        
        # Vetor U = B - A
        Ux = B[0] - A[0]
        Uy = B[1] - A[1]
        Uz = B[2] - A[2]
        
        # Vetor V = C - A
        Vx = C[0] - A[0]
        Vy = C[1] - A[1]
        Vz = C[2] - A[2]
        
        # Produto Vetorial (Cross Product): N = U x V
        Nx = (Uy * Vz) - (Uz * Vy)
        Ny = (Uz * Vx) - (Ux * Vz)
        Nz = (Ux * Vy) - (Uy * Vx)
        
        # Normalização
        modulo = math.sqrt(Nx**2 + Ny**2 + Nz**2)
        
        if modulo == 0: return (0, 0, 0) # Evita divisão por zero
        return (Nx/modulo, Ny/modulo, Nz/modulo)


        
class Cubo:
    # So precisamos de um vértice e a medida do lado pra definir um cubo
    # v0 poderia ser o local do clique do mouse
    def __init__(self, v0, lado, ka, kd, ks): 

        # Dados básicos: material, topologia inicial, faces

        self.ka = (ka[0], ka[1], ka[2]) #(r, g, b)
        self.kd = (kd[0], kd[1], kd[2])  
        self.ks = (ks[0], ks[1], ks[2], ks[3]) #(r, g, b, n)
        
        x, y, z = v0[0], v0[1], v0[2]
        l = lado

        v0 = (x,     y,     z,     1) # Trás-Esq-Baixo
        v1 = (x + l, y,     z,     1) # Trás-Dir-Baixo
        v2 = (x,     y + l, z,     1) # Trás-Esq-Cima
        v3 = (x + l, y + l, z,     1) # Trás-Dir-Cima
        
        v4 = (x,     y,     z + l, 1) # Frente-Esq-Baixo
        v5 = (x + l, y,     z + l, 1) # Frente-Dir-Baixo
        v6 = (x,     y + l, z + l, 1) # Frente-Esq-Cima
        v7 = (x + l, y + l, z + l, 1) # Frente-Dir-Cima
        
        self.lista_vertices = (v0, v1, v2, v3, v4, v5, v6, v7)

        # Faces em sentido anti-horário
        face0 = Face(v4, v5, v7, v6) # Frente
        face1 = Face(v1, v0, v2, v3) # Traś
        face2 = Face(v0, v4, v6, v2) # Direita
        face3 = Face(v5, v1, v3, v7) # Esquerda
        face4 = Face(v2, v6, v7, v3) # Topo
        face5 = Face(v4, v0, v1, v5) # Base

        self.lista_faces = (face0, face1, face2, face3, face4, face5)

        # Dados do mundo

        self.rotacao = (0.0, 0.0, 0.0) # Rotação atual
        self.escala = 1.0 # Rotação atual
        self.trans = (0.0, 0.0, 0.0) #Posição atual
    
    def get_model_matrix(self):
        matriz = Mat4.identity()
        

class Camera:
    def __init__(self, vrp, vpn, vup):
        self.vrp = (vrp[0], vrp[1], vrp[2])
        self.vpn = (vpn[0], vpn[1], vpn[2])
        self.vup = (vup[0], vup[1], vpn[2])

        self.prp = (0.0, 0.0, 1.0) 
        
        # Distância focal (d) 
        self.distancia_focal = 1.0
        
        # Janela 
        # Define a abertura da lente (Zoom)
        # u_min, u_max, v_min, v_max
        self.window = {"u_min" : -1.0, "u_max": 1.0,
                       "v_min" : -1.0, "v_max" : 1.0}
        
        # Planos de Recorte (Clipping) para definir o Volume de Visão
        self.near = 1.0    # Distância mínima (Z min)
        self.far = 100.0   # Distância máxima (Z max)

    def get_matrix(self):
        # Todo: Retornar M_View * M_Projection
        pass

class Luz:
    # Constantes para legibilidade
    PONTUAL = 1 #fonte de luz na cena
    DIRECIONAL = 2 #fonte de luz no infinito

    def __init__(self, tipo, vetor_pos_dir, intensidade_rgb_s, intensidade_rgb_d):
        self.tipo = tipo  # Luz.PONTUAL ou Luz.DIRECIONAL
        
        # Se for PONTUAL, vetor_pos_dir é a Posição (x, y, z)
        # Se for DIRECIONAL, vetor_pos_dir é a Direção (dx, dy, dz)
        self.posicao_ou_direcao = (vetor_pos_dir[0], vetor_pos_dir[1], vetor_pos_dir[2]) 
        
        # Intensidades da Fonte Luminosa
        # Cor da luz
        self.id = (intensidade_rgb_d[0], intensidade_rgb_d[1], intensidade_rgb_d[2])  # Intensidade Difusa (RGB)
        self.i_spec = (intensidade_rgb_s[0], intensidade_rgb_s[1], intensidade_rgb_s[2])  # Intensidade Especular (Geralmente igual à difusa)

class Cena:
    def __init__(self, width, height):
        # --- Gerenciamento de Objetos ---
        self.objetos = []     # Lista de instâncias de Cubo
        self.luzes = []       # Lista de instâncias de Luz
        self.camera = None    # Instância de Camera
        
        # Luz Ambiente Global (Ilumina todas as faces minimamente)
        self.ia = (0.1, 0.1, 0.1) # Cinza escuro fraco

        # --- Viewport (Dimensões da Tela/Janela do SO) ---
        self.viewport = {
            'x_min': 0, 'y_min': 0,
            'x_max': width, 'y_max': height
        }
        self.width = width
        self.height = height

        # --- Buffers de Rasterização (Alocação de Memória) ---
        # ColorBuffer: Matriz width x height guardando tuplas (R, G, B)
        # Uma entrada para cada pixel
        # Inicializa tudo com preto (0,0,0)
        self.color_buffer = [[(0, 0, 0) for _ in range(height)] for _ in range(width)]
        
        # DepthBuffer (Z-Buffer): Matriz width x height guardando floats
        # Inicializa com infinito positivo (qualquer objeto será menor que infinito)
        self.depth_buffer = [[float('inf') for _ in range(height)] for _ in range(width)]

    def adicionar_objeto(self, cubo):
        self.objetos.append(cubo)

    def adicionar_luz(self, luz):
        self.luzes.append(luz)

    def definir_camera(self, camera):
        self.camera = camera

    def limpar_buffers(self):
        # Reinicia os buffers para o próximo frame
        # Pinta fundo de preto e Z-buffer de infinito
        for x in range(self.width):
            for y in range(self.height):
                self.color_buffer[x][y] = (0, 0, 0) # Cor de fundo
                self.depth_buffer[x][y] = float('inf')

    def renderizar(self):
        # Aqui entrará o pipeline principal:
        # 1. Limpar Buffers
        # 2. Calcular matrizes
        # 3. Para cada objeto -> Rasterizar
        pass