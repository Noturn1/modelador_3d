import math

class Mat4:

    def identity(self):
        return [

            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]

        ]

    def null(self):
        return [
            
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]

        ]
    
    def trans(self, dx, dy, dz):
        return [
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1 ]
        ]
    
    def scale(self, sx, sy, sz):
        return [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0,  1]
        ]
    
    def rotate_z(self, tetha):
        #a biblioteca aceita radianos
        #o usuario envia o parâmetro em graus, e a conversão ocorre aqui
        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        return[

            [cos, -sen, 0, 0],
            [sen,  cos, 0, 0],
            [0,    0,   1, 0],
            [0,    0,   0, 1]
        ]
    
    def rotate_y(self, tetha):

        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        return[
            [cos,  0, sen,  0],
            [0,    1, 0,    0],
            [-sen, 0, cos,  0],
            [0,    0, 0,    1]
        ]
    
    def rotate_x(self, tetha):

        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        return[
            [1, 0,   0,      0],
            [0, cos, -sen,   0],
            [0, sen, cos,    0],
            [0, 0,   0,      1]
        ]
    
    def mul(self, mat1, mat2):

        res = [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ]

        # 2. Algoritmo de Multiplicação (Linha x Coluna)
        # C[i][j] = Somatório(A[i][k] * B[k][j])
        for i in range(4):           # Percorre as linhas de mat1
            for j in range(4):       # Percorre as colunas de mat2
                for k in range(4):   # Percorre o elemento comum
                    res[i][j] += mat1[i][k] * mat2[k][j]

        return res
    
    def mul_point(self, mat, ponto):
        # ponto deve ser uma tupla ou lista (x, y, z, w)
        # O resultado é um novo ponto transformado
        
        res = [0.0, 0.0, 0.0, 0.0]
        
        for i in range(4): # Para cada linha da matriz
            soma = 0.0
            for j in range(4): # Multiplica pela coluna do vetor
                soma += mat[i][j] * ponto[j]
            res[i] = soma
            
        return res    



class Face:
    # define a face do objeto, vertices são lista [x,y,z]

    def __init__(self, v0, v1, v2, v3):

        #face do mundo
        self.lista_vertices = (v0, v1, v2, v3) 

        #face qua vai sofrer transforamções
        self.model_faces = [v0, v1, v1, v2, v3]

        self.normal = self.calcular_normal(self)         

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

        self.ka = [ka[0], ka[1], ka[2]] #(r, g, b)
        self.kd = [kd[0], kd[1], kd[2]]  
        self.ks = [ks[0], ks[1], ks[2], ks[3]] #(r, g, b, n)
        
        x, y, z = v0[0], v0[1], v0[2]
        l = lado

        #não sofre transformações
        v0 = (x,     y,     z,     1) # Trás-Esq-Baixo
        v1 = (x + l, y,     z,     1) # Trás-Dir-Baixo
        v2 = (x,     y + l, z,     1) # Trás-Esq-Cima
        v3 = (x + l, y + l, z,     1) # Trás-Dir-Cima)
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
        
        #faces que vão sofrer alterações
        self.model_faces = [face0, face1, face2, face3, face4, face5]
        # Dados do mundo

        #matrix que vai sofrer transformações e ser rasterizada

        self.model_matrix = [ 
            [v0[0],v1[0],v2[0],v3[0],v4[0],v5[0],v6[0],v7[0]],
            [v0[1],v1[1],v2[1],v3[1],v4[1],v5[1],v6[1],v7[1]],
            [v0[2],v1[2],v2[2],v3[2],v4[2],v5[2],v6[2],v7[2]],
            [1,    1,    1,    1,    1,    1,    1,    1    ]
        ]        

        self.rotacao = [0.0, 0.0, 0.0] # Rotação atual
        self.escala = 1.0 # Rotação atual
        self.trans = [0.0, 0.0, 0.0] #Posição atual
    
    def get_model_matrix(self):
        matriz = Mat4.identity()
        

class Camera:
    def __init__(self, vrp, vpn, vup):
        self.vrp = [vrp[0], vrp[1], vrp[2]]
        self.vpn = [vpn[0], vpn[1], vpn[2]]
        self.vup = [vup[0], vup[1], vpn[2]]

        self.prp = [0.0, 0.0, 1.0] 
        
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
        self.posicao_ou_direcao = [vetor_pos_dir[0], vetor_pos_dir[1], vetor_pos_dir[2]] 
        
        # Intensidades da Fonte Luminosa
        # Cor da luz
        self.id = [intensidade_rgb_d[0], intensidade_rgb_d[1], intensidade_rgb_d[2]]  # Intensidade Difusa (RGB)
        self.i_spec = [intensidade_rgb_s[0], intensidade_rgb_s[1], intensidade_rgb_s[2]]  # Intensidade Especular (Geralmente igual à difusa)

class Cena:
    def __init__(self, width, height):
        # --- Gerenciamento de Objetos ---
        self.objetos = []     # Lista de instâncias de Cubo
        self.luzes = []       # Lista de instâncias de Luz
        self.camera = None    # Instância de Camera
        
        # Luz Ambiente Global (Ilumina todas as faces minimamente)
        self.ia = [0.1, 0.1, 0.1] # Cinza escuro fraco

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
                self.color_buffer[x][y] =[0, 0, 0] # Cor de fundo
                self.depth_buffer[x][y] = float('inf')

    def renderizar(self):
        # Aqui entrará o pipeline principal:
        # 1. Limpar Buffers
        # 2. Calcular matrizes
        # 3. Para cada objeto -> Rasterizar
        pass