import math


class Vector:

#Classe para operações de vetor/ponto (x, y, z)
#staticmethod permite chamar o metodo sem precisar incializar a classe
    @staticmethod   
    def create_vector(A, B):
        Vx = B[0] - A[0]
        Vy = B[1] - A[1]
        Vz = B[2] - A[2]
        
        return [Vx, Vy, Vz]

    @staticmethod
    def normalize(V):
        mag = math.sqrt(V[0]**2 + V[1]**2 + V[2]**2)
        
        if mag == 0:
            return [0, 0, 0]
        
        return [
            V[0] / mag,
            V[1] / mag,
            V[2] / mag,
            
        ]

    @staticmethod
    def mul(mat, ponto):
        # função pra aplicar transformação em um vetor/ponto
        # ponto deve ser uma tupla ou lista (x, y, z, w)
        # O resultado é um novo ponto transformado
            
        res = [0.0, 0.0, 0.0, 0.0]
            
        for i in range(4): # Para cada linha da matriz
            soma = 0.0
            for j in range(4): # Multiplica pela coluna do vetor
                soma += mat[i][j] * ponto[j]
            res[i] = soma
                
        return res    
    
    @staticmethod
    def cross_product(A, B):
        #função para calcular produto vetorial
        # recebe dois vetores (x, y, z)    
        
        Ux = A[0]
        Uy = A[1]
        Uz = A[2]

        
        Vx = B[0]
        Vy = B[1]
        Vz = B[2]

        # Produto Vetorial (Cross Product): N = U x V
        Nx = (Uy * Vz) - (Uz * Vy)
        Ny = (Uz * Vx) - (Ux * Vz)
        Nz = (Ux * Vy) - (Uy * Vx)

        return (Nx, Ny, Nz)
    
    @staticmethod
    def dot_product(A,B):
    # Calcula o produto escalar de dois vetores (x, y, z)
        return (A[0] * B[0]) + (A[1] * B[1]) + (A[2] * B[2])



class Pipeline:
    # Adaptado do artigo de Alvy-Ray Smith
    # todas as matrizes são transpostas, para trabalhar na regra da mão direita

    @staticmethod
    def get_matrix_A(Viewpoint):

        return[
            [1, 0, 0, -Viewpoint[0]],
            [0, 1, 0, -Viewpoint[1]],
            [0, 0, 1, -Viewpoint[2]],
            [0, 0, 0, 1           ]
            ]
    
    @staticmethod
    #recebe vetores (x, y, z) como parâmetro
    def get_matrix_B(u, v, n):

        return[
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [n[0], n[1], n[2], 0],
            [0,    0,    0,    1]
        ]
    
    @staticmethod 
    def get_matrix_C(Cu, Cv, d):

        return[
            [1, 0, -Cu/d,  0],
            [0, 1, -Cv/d,  0],
            [0, 0,  1,     0],
            [0, 0,  0,     1]
        ]

    @staticmethod
    def get_matrix_D(Su, Sv, d, f):

        return [
            [d/(Su*f), 0,        0,   0],
            [0,        d/(Sv*f), 0,   0],
            [0,        0,        1/f, 0],
            [0,        0,        0,   1]
        ]

    @staticmethod
    def get_matrix_P(far, near):

        return [
            [1, 0, 0,           0                 ],
            [0, 1, 0,           0                 ],
            [0, 0, far/(far - near), (-near)/(far-near)],
            [0, 0, 1,           0                 ]
        ]        
    
    @staticmethod
    def get_matrix_J():

        return[
            [1, 0, 0,  0],
            [0, -1, 0,  0],
            [0, 0, 1, 0],
            [0, 0, 0,  1]     
        ]
    
    @staticmethod
    def get_matrix_K():

        return[
            [0.5, 0,   0, 0.5],
            [0,   0.5, 0, 0.5],
            [0,   0,   1, 0  ],
            [0,   0,   0, 1  ]
        ]

    @staticmethod
    def get_matrix_L(x_max, x_min, y_max, y_min, z_max, z_min):

        return[
            [x_max - x_min, 0,             0,              x_min],
            [0,             y_max - y_min, 0,              y_min],
            [0,             0,             z_max - z_min,  z_min],
            [0,             0,              0,             1    ]
        ]
    
    @staticmethod
    def get_matrix_M():

        return[
            [1,   0,     0,     0.5],
            [0,   1,     0,     0.5],
            [0,   0,     1,     0.5],
            [0,   0,     0,     1  ]
        ]



class Mat4:

# Classe para operações de matriz (4x4)
    @staticmethod
    def print_matrix(M):
        for line in M:
            print(line)


    @staticmethod
    def identity():
        return [

            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]

        ]

    @staticmethod
    def null():
        return [
            
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]

        ]
    
    @staticmethod
    def trans(dx, dy, dz):
        return [
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1 ]
        ]
    
    @staticmethod
    def scale(sx, sy, sz):
        return [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0,  1]
        ]
    
    @staticmethod
    def rotate_z(tetha):
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
    
    @staticmethod
    def rotate_y(tetha):

        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        return[
            [cos,  0, sen,  0],
            [0,    1, 0,    0],
            [-sen, 0, cos,  0],
            [0,    0, 0,    1]
        ]
    
    @staticmethod
    def rotate_x(tetha):

        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        return[
            [1, 0,   0,      0],
            [0, cos, -sen,   0],
            [0, sen, cos,    0],
            [0, 0,   0,      1]
        ]
    
    @staticmethod
    def mul(mat1, mat2):
        #essa função é melhor aplicada para compor matrizes
        res = Mat4.null()

        for i in range(4):            
            for j in range(4):       
                for k in range(4):   
                    res[i][j] += mat1[i][k] * mat2[k][j]

        return res




class Face:
    # define a face do objeto, vertices são lista [x,y,z]

    def __init__(self, i0, i1, i2, i3):

        #face do mundo
        self.indices = (i0, i1, i2, i3)

        #calcular normal (já normalizado)
        self.normal = None        

        
class Cubo:


    def print_vertices(self):
        i = 0
        for v in self.vertices_modelo_transformados:
            print(f"v{i}: {v}")
            i += 1


    def aplicar_transformacao(self, mat):
        novos_vertices = []

        for v in self.vertices_modelo_transformados:
            vt = Vector.mul(mat, v)
            novos_vertices.append(list(vt))

        self.vertices_modelo_transformados = novos_vertices
        self.atualizar_normais()
        self.calcular_centroide()


    def atualizar_normais(self):
        for face in self.lista_faces:
            i0, i1, i2, i3 = face.indices

            A = self.vertices_modelo_transformados[i0]
            B = self.vertices_modelo_transformados[i1]
            C = self.vertices_modelo_transformados[i3]

            AB = (B[0]-A[0], B[1]-A[1], B[2]-A[2])
            AC = (C[0]-A[0], C[1]-A[1], C[2]-A[2])

            face.normal = Vector.cross_product(AB, AC)



    def calcular_centroide(self):
            # Inicializa acumuladores para X, Y, Z
            soma_x = 0.0
            soma_y = 0.0
            soma_z = 0.0
            
            num_vertices = len(self.vertices_modelo_transformados)
            
            # Percorre todos os vértices do cubo
            for v in self.vertices_modelo_transformados:
                soma_x += v[0] # Soma X
                soma_y += v[1] # Soma Y
                soma_z += v[2] # Soma Z
                # O v[3] é o W, nós ignoramos ele propositalmente
                
            # Calcula a média aritmética
            cx = soma_x / num_vertices
            cy = soma_y / num_vertices
            cz = soma_z / num_vertices
            
            return cx, cy, cz
             


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

        
        self.vertices_modelo = [v0, v1, v2, v3, v4, v5, v6, v7]
        self.vertices_modelo_transformados = list(self.vertices_modelo)

        # Faces em sentido anti-horário
        face0 = Face(4, 5, 7, 6) # Frente
        face1 = Face(1, 0, 2, 3) # Traś
        face2 = Face(0, 4, 6, 2) # Direita
        face3 = Face(5, 1, 3, 7) # Esquerda
        face4 = Face(2, 6, 7, 3) # Topo
        face5 = Face(4, 0, 1, 5) # Base



        self.lista_faces = (face0, face1, face2, face3, face4, face5)
        
        #faces que vão sofrer alterações
        self.model_faces = [face0, face1, face2, face3, face4, face5]
        # Dados do mundo
   
        #matrix que vai sofrer transformações e ser rasterizada
        
        self.rotacao = [0.0, 0.0, 0.0] # Rotação atual
        self.escala = 1.0 # escala atual
        self.atualizar_normais()
        self.centroide = self.calcular_centroide()

        self.trans = [self.centroide[0], self.centroide[1], self.centroide[2]] #Posição atual (referência no centróide)
            

class Camera:

    def get_view_spec(self):
        return (self.u, self.v, self.n)

    def cal_view_spec(self):
        #função para calcular o view spec (página 4 do artigo do Alvy-Ray)
        
        n = Vector.normalize(self.N)

        up = Vector.normalize(self.Y)

        dot = Vector.dot_product(up, n) 
        
        vx = up[0] - (dot * n[0])
        vy = up[1] - (dot * n[1])
        vz = up[2] - (dot * n[2])
        
        v_temp = [vx, vy, vz]
        v = Vector.normalize(v_temp)

        #calcular vetor u (invertido pra usar a regra da mão direita)
        u = Vector.normalize(Vector.cross_product(v, n))

        return u, v, n
    


    def __init__(self, vrp, P, Y, u_max, u_min, v_max, v_min, DP, near, far,
                 x_min, x_max, y_min, y_max, Vres, Hres):
        
        self.vrp = [vrp[0], vrp[1], vrp[2]]
        self.N = Vector.create_vector(vrp, P)
        self.Y = [Y[0], Y[1], Y[2]]

        self.u, self.v, self.n = self.cal_view_spec()
     
        # Distância focal (d) 
        self.DP = DP
        
        # Janela 
        # Define a abertura da lente (Zoom)
        # u_min, u_max, v_min, v_max
        self.viewport = {"x_min" : x_min, "x_max" : x_max,
                         "y_min" : y_min, "y_max" : y_max}      

        self.z_min = near/far
        self.z_max = 1
        self.Vres = Vres
        self.Hres = Hres
    

        self.window = {"u_min" : u_min, "u_max": u_max,
                       "v_min" : v_min, "v_max" : v_max}
        
        self.Cu = (self.window["u_max"] + self.window["u_min"]) / 2
        self.Cv = (self.window["v_max"] + self.window["v_min"]) / 2
        self.Su = (self.window["u_max"] - self.window["u_min"])
        self.Sv = (self.window["v_max"] - self.window["v_min"])
        self.AR = self.Su/self.Sv
        self.PAR = self.AR*(self.Vres/self.Hres)

        # Planos de Recorte (Clipping) para definir o Volume de Visão
        self.near = near    # Distância mínima (Z min)
        self.far = far   # Distância máxima (Z max)

class VerticeWA:
    # Estrutura auxiliar para as listas duplamente encadeadas do Weiler-Atherton
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.is_intersecao = False
        self.is_entrada = False # True = Entrando no Clip, False = Saindo
        self.visitado = False
        self.proximo = None      # Ponteiro para o próximo vértice na lista do polígono
        self.proximo_clip = None # Ponteiro para a lista da janela de recorte
        self.alpha = 0.0         # Fator paramétrico (0 a 1) para ordenação de interseções

    def __repr__(self):
        tipo = "INT" if self.is_intersecao else "VERT"
        dir = "(ENTRADA)" if self.is_entrada else "(SAIDA)" if self.is_intersecao else ""
        return f"{tipo}: ({self.x:.1f}, {self.y:.1f}) {dir}"


class RenderPoligon:
    #classe para definir o polígono renderizavel, guardando vertices do cubo após recorte
    #evitar mudar a classe cubo, pra não afetar o trabalho dos outros
    #representa uma face, que é a unidade basica a ser renderizada
    def __init__(self, vertices_2d, ka, kd, ks, normal):
        self.vertices_2d = vertices_2d
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.normal = normal


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
    def __init__(self, height, width):
        # --- Gerenciamento de Objetos ---
        self.objetos = []     # Lista de instâncias de Cubo
        self.luzes = []       # Lista de instâncias de Luz
        self.camera = None    # Instância de Camera
        self.height = height
        self.width = width
        self.obejetos = []
        
        # Luz Ambiente Global (Ilumina todas as faces minimamente)
        self.ia = [0.1, 0.1, 0.1] # Cinza escuro fraco

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

    def recorteWA(face_ndc):
        #algoritmo de recorte Weiler-Atherton
        # face_ndc é uma instância da classe RenderPoligon
        # vertices_face_ndc é uma lista com 4 pontos [(x0,y0), (x1,y1), (x2,y2), (x3,y3)]
        
        # 1. Definir a janela de recorte NDC (-1 a 1)
        janela_x_min = Camera.viewport["x_min"]
        janela_x_max = Camera.viewport["x_max"]
        janela_y_min = Camera.viewport["y_min"]
        janela_y_max = Camera.viewport["y_max"]

        v0 = VerticeWA(janela_x_min, janela_y_min)
        v1 = VerticeWA(janela_x_max, janela_y_min)
        v2 = VerticeWA(janela_x_max, janela_y_max)
        v3 = VerticeWA(janela_x_min, janela_y_max)

        # 2. Executar o algoritmo de Weiler-Atherton
        
        # O algoritmo retorna uma lista de polígonos visíveis.
        # Exemplo: um pentágono resultante de um corte de quina.
        # Retorno: [ [(x1,y1), (x2,y2), (x3,y3), (x4,y4), (x5,y5)] ]
        print()           



    @staticmethod
    def inserir_vertice_ordenado(p_inicio, p_fim, novo_vertice):
        atual = p_inicio
        # Procura a posição correta baseada no 'alpha' (distância do início da reta)
        while atual.proximo != p_fim and atual.proximo.alpha < novo_vertice.alpha:
            atual = atual.proximo
        
        # Insere o novo_vertice na corrente
        novo_vertice.proximo = atual.proximo
        atual.proximo = novo_vertice


    @staticmethod
    def calcular_intersecao(p1, p2, p3, p4):
        """
        Calcula a interseção entre o segmento A (p1->p2) e B (p3->p4).
        Retorna (x, y, t) ou None se não houver cruzamento.
        """
        denominador = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)

        if abs(denominador) < 1e-6:
            # as multíplicações de matriz geram muito erro de ponto flutuante
            # acaba saindo muitos valores proximos de zero, que deveriam ser zero
            # se não fizer isso, a conta aqui embaixo quebra pq divide por um numero muito pequenp
            return None # considera as linhas paralelas

        # t = posição da interseção na reta 1 (Face)
        t = ((p1.x - p3.x) * (p3.y - p4.y) - (p1.y - p3.y) * (p3.x - p4.x)) / denominador
        # u = posição da interseção na reta 2 (Janela)
        u = ((p1.x - p3.x) * (p1.y - p2.y) - (p1.y - p3.y) * (p1.x - p2.x)) / denominador

        if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
            int_x = p1.x + t * (p2.x - p1.x)
            int_y = p1.y + t * (p2.y - p1.y)
            return (int_x, int_y, t)

        return None


    def recorteWA(self, vertices_face_ndc):
        # passo 1: definir a janela de recorte
        xmin = self.camera.viewport["x_min"]
        xmax = self.camera.viewport["x_max"]
        ymin = self.camera.viewport["y_min"]
        ymax = self.camera.viewport["y_max"]
        
        # cria os vértices da janela no sentido horário
        janela = [
            VerticeWA(xmin, ymin), # v0: Fundo-Esq
            VerticeWA(xmax, ymin), # v1: Fundo-Dir
            VerticeWA(xmax, ymax), # v2: Topo-Dir
            VerticeWA(xmin, ymax)  # v3: Topo-Esq
        ]
        # encadear os vértices da janela
        for i in range(4):
            janela[i].proximo = janela[(i + 1) % 4]

        # passo2: criar a lista da face
        sujeito = []
        for v in vertices_face_ndc:
            sujeito.append(VerticeWA(v[0], v[1], v[2])) # x, y, z

        for i in range(len(sujeito)):
            sujeito[i].proximo = sujeito[(i + 1) % len(sujeito)]

        # passo 3: calcular intercessões entre a janela e a face
        for i in range(len(sujeito)):
            p1 = sujeito[i]
            p2 = sujeito[(i + 1) % len(sujeito)]

            for j in range(4):
                p3 = janela[j]
                p4 = janela[(j + 1) % 4]

                intersecao = self.calcular_intersecao(p1, p2, p3, p4)
                
                if intersecao:
                    ix, iy, t = intersecao
                    
                    # 1. Cria o vértice para a lista da fave
                    int_sujeito = VerticeWA(ix, iy)
                    int_sujeito.is_intersecao = True
                    int_sujeito.alpha = t # 't' da reta da face
                    
                    # 2. Cria o vértice (gêmeo) para a lista da Janela
                    u = ((ix - p3.x) * (p4.x - p3.x) + (iy - p3.y) * (p4.y - p3.y)) / ((p4.x - p3.x)**2 + (p4.y - p3.y)**2)
                    int_janela = VerticeWA(ix, iy)
                    int_janela.is_intersecao = True
                    int_janela.alpha = u # 'u' da reta da janela

                    # Linka os gêmeos (O "troca-trilho" do algoritmo)
                    int_sujeito.proximo_clip = int_janela
                    int_janela.proximo_clip = int_sujeito

                    # Define Entrada/Saída
                    p2_dentro = (xmin <= p2.x <= xmax) and (ymin <= p2.y <= ymax)
                    int_sujeito.is_entrada = p2_dentro
                    int_janela.is_entrada = p2_dentro

                    # Insere nas listas
                    self.inserir_vertice_ordenado(p1, p2, int_sujeito)
                    self.inserir_vertice_ordenado(p3, p4, int_janela)

        # passo 4: varrer a lista e ligar os poligonos
        poligonos_recortados = []
        
        atual = sujeito[0]
        for _ in range(len(sujeito) * 2): # Limite de segurança contra loops infinitos
            if atual.is_intersecao and atual.is_entrada and not atual.visitado:
                novo_poligono = []
                p_nav = atual
                
                while not p_nav.visitado:
                    p_nav.visitado = True
                    novo_poligono.append((p_nav.x, p_nav.y))
                    
                    if p_nav.is_intersecao:
                        p_nav.proximo_clip.visitado = True # Marca o gêmeo como visitado
                        if p_nav.is_entrada:
                            p_nav = p_nav.proximo # ENTRADA: Segue o Sujeito
                        else:
                            p_nav = p_nav.proximo_clip.proximo # SAÍDA: Segue a Janela
                    else:
                        p_nav = p_nav.proximo # Vértice comum
                
                poligonos_recortados.append(novo_poligono)

            atual = atual.proximo

        # CASO ESPECIAL: O polígono está 100% dentro da tela
        if len(poligonos_recortados) == 0:
            if (xmin <= sujeito[0].x <= xmax) and (ymin <= sujeito[0].y <= ymax):
                poligono_2d = [(v[0], v[1]) for v in vertices_face_ndc]
                return [poligono_2d] 

        return poligonos_recortados


    def renderizar(self, cubos, camera):
        # Aqui entrará o pipeline principal:
        # 1. Limpar Buffers
        self.limpar_buffers()
        # 2. Calcular matrizes
        # 3. Para cada objeto -> Rasterizar
        pass