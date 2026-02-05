import math


class VerticeTela:
    """
    Representa um vértice já projetado no espaço de tela (Screen Space).
    Armazena x, y (inteiros para pixel), z (para buffer), cor e normal (para iluminação).
    """

    def __init__(self, x, y, z, cor=None, normal=None):
        self.x = x
        self.y = y
        self.z = z  # Profundidade
        self.cor = cor  # Tupla (r, g, b) para Objeto cor
        self.normal = normal  # Tupla (nx, ny, nz) para Phong


class Vector:

    # Classe para operações de vetor/ponto (x, y, z)
    # staticmethod permite chamar o metodo sem precisar incializar a classe

    @staticmethod
    def norm(V):
        # Calcula a soma dos quadrados dos componentes
        soma_quadrados = 0.0
        for componente in V:
            soma_quadrados += componente**2

        # Retorna a raiz quadrada da soma
        return math.sqrt(soma_quadrados)

    @staticmethod
    def create_vector(A, B):
        Vx = B[0] - A[0]
        Vy = B[1] - A[1]
        Vz = B[2] - A[2]

        return [Vx, Vy, Vz]

    @staticmethod
    def normalize(V):
        mag = math.sqrt(V[0] ** 2 + V[1] ** 2 + V[2] ** 2)

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

        for i in range(4):  # Para cada linha da matriz
            soma = 0.0
            for j in range(4):  # Multiplica pela coluna do vetor
                soma += mat[i][j] * ponto[j]
            res[i] = soma

        return res

    @staticmethod
    def cross_product(A, B):
        # função para calcular produto vetorial
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
    def dot_product(A, B):
        # Calcula o produto escalar de dois vetores (x, y, z)
        return (A[0] * B[0]) + (A[1] * B[1]) + (A[2] * B[2])


class Pipeline:
    # Adaptado do artigo de Alvy-Ray Smith
    # todas as matrizes são transpostas, para trabalhar na regra da mão direita

    @staticmethod
    def get_matrix_A(Viewpoint):

        return [
            [1, 0, 0, -Viewpoint[0]],
            [0, 1, 0, -Viewpoint[1]],
            [0, 0, 1, -Viewpoint[2]],
            [0, 0, 0, 1],
        ]

    @staticmethod
    # recebe vetores (x, y, z) como parâmetro
    def get_matrix_B(u, v, n):

        return [
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [n[0], n[1], n[2], 0],
            [0, 0, 0, 1],
        ]

    @staticmethod
    def get_matrix_C(Cu, Cv, d):

        return [[1, 0, -Cu / d, 0], [0, 1, -Cv / d, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    @staticmethod
    def get_matrix_D(Su, Sv, d, f):

        return [
            [d / (Su * f), 0, 0, 0],
            [0, d / (Sv * f), 0, 0],
            [0, 0, 1 / f, 0],
            [0, 0, 0, 1],
        ]

    @staticmethod
    def get_matrix_P(far, near):

        return [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, far / (far - near), (-near) / (far - near)],
            [0, 0, 1, 0],
        ]

    @staticmethod
    def get_matrix_J():

        return [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    @staticmethod
    def get_matrix_K():

        return [[0.5, 0, 0, 0.5], [0, 0.5, 0, 0.5], [0, 0, 1, 0], [0, 0, 0, 1]]

    @staticmethod
    def get_matrix_L(x_max, x_min, y_max, y_min, z_max, z_min):

        return [
            [x_max - x_min, 0, 0, x_min],
            [0, y_max - y_min, 0, y_min],
            [0, 0, z_max - z_min, z_min],
            [0, 0, 0, 1],
        ]

    @staticmethod
    def get_matrix_M():

        return [[1, 0, 0, 0.5], [0, 1, 0, 0.5], [0, 0, 1, 0.5], [0, 0, 0, 1]]


class Mat4:

    # Classe para operações de matriz (4x4)
    @staticmethod
    def print_matrix(M):
        for line in M:
            print(line)

    @staticmethod
    def identity():
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    @staticmethod
    def null():
        return [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ]

    @staticmethod
    def trans(dx, dy, dz):
        return [[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]]

    @staticmethod
    def scale(sx, sy, sz, centroide):
        
        escala = [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
        trans_centroide_ida = Mat4.trans(-centroide[0], -centroide[1], -centroide[2])
        trans_centroide_volta = Mat4.trans(centroide[0], centroide[1], centroide[2])

        escala_centroide = Mat4.mul(escala, trans_centroide_ida)
        return(Mat4.mul(trans_centroide_volta, escala_centroide))

    @staticmethod
    def rotate_z(tetha, centroide):
        # a biblioteca aceita radianos
        # o usuario envia o parâmetro em graus, e a conversão ocorre aqui
        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        trans_centroide_ida = Mat4.trans(-centroide[0], -centroide[1], -centroide[2])
        trans_centroide_volta = Mat4.trans(centroide[0], centroide[1], centroide[2])

        rotate_z = [[cos, -sen, 0, 0], [sen, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        rotate_z_centroide = Mat4.mul(rotate_z, trans_centroide_ida)


        return(Mat4.mul(trans_centroide_volta, rotate_z_centroide))
  

    @staticmethod
    def rotate_y(tetha, centroide):

        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)


        trans_centroide_volta = Mat4.trans(centroide[0], centroide[1], centroide[2])
        trans_centroide_ida = Mat4.trans(-centroide[0], -centroide[1], -centroide[2])
        rotate_y = [[cos, 0, sen, 0], [0, 1, 0, 0], [-sen, 0, cos, 0], [0, 0, 0, 1]]
        
        rotate_y_centroide = Mat4.mul(rotate_y, trans_centroide_ida)

        return(Mat4.mul(trans_centroide_volta, rotate_y_centroide))

    @staticmethod
    def rotate_x(tetha, centroide):

        tetha_rad = math.radians(tetha)
        cos = math.cos(tetha_rad)
        sen = math.sin(tetha_rad)

        trans_centroide_ida = Mat4.trans(-centroide[0], -centroide[1], -centroide[2])
        rotate_x = [[1, 0, 0, 0], [0, cos, -sen, 0], [0, sen, cos, 0], [0, 0, 0, 1]]

        rotate_x_centroide = Mat4.mul(rotate_x, trans_centroide_ida)
        trans_centroide_volta = Mat4.trans(centroide[0], centroide[1], centroide[2])


        return(Mat4.mul(trans_centroide_volta, rotate_x_centroide))

    @staticmethod
    def mul(mat1, mat2):
        # essa função é melhor aplicada para compor matrizes
        res = Mat4.null()

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    res[i][j] += mat1[i][k] * mat2[k][j]

        return res


class Face:
    # define a face do objeto, vertices são lista [x,y,z]

    def __init__(self, i0, i1, i2, i3):

        # face do mundo
        self.indices = (i0, i1, i2, i3)

        # calcular normal (já normalizado)
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
        self.centroide = self.calcular_centroide()

    def atualizar_normais(self):
        # 1. Calcular e normalizar as normais das faces
        for face in self.lista_faces:
            i0, i1, i2, i3 = face.indices

            A = self.vertices_modelo_transformados[i0]
            B = self.vertices_modelo_transformados[i1]
            C = self.vertices_modelo_transformados[i3]

            AB = (B[0] - A[0], B[1] - A[1], B[2] - A[2])
            AC = (C[0] - A[0], C[1] - A[1], C[2] - A[2])

            normal = Vector.cross_product(AB, AC)
            face.normal = Vector.normalize(normal)

        # 2. Calcular normais de vértice (média das normais das faces adjacentes)
        num_vertices = len(self.vertices_modelo_transformados)
        self.normais_vertices = [(0, 0, 0)] * num_vertices

        for idx_vertice in range(num_vertices):
            soma_nx, soma_ny, soma_nz = 0.0, 0.0, 0.0
            count = 0

            # Encontrar todas as faces que contêm este vértice
            for face in self.lista_faces:
                if idx_vertice in face.indices:
                    soma_nx += face.normal[0]
                    soma_ny += face.normal[1]
                    soma_nz += face.normal[2]
                    count += 1

            # Calcular média e normalizar
            if count > 0:
                media = (soma_nx / count, soma_ny / count, soma_nz / count)
                self.normais_vertices[idx_vertice] = Vector.normalize(media)

    def calcular_centroide(self):
        # Inicializa acumuladores para X, Y, Z
        soma_x = 0.0
        soma_y = 0.0
        soma_z = 0.0

        num_vertices = len(self.vertices_modelo_transformados)

        # Percorre todos os vértices do cubo
        for v in self.vertices_modelo_transformados:
            soma_x += v[0]  # Soma X
            soma_y += v[1]  # Soma Y
            soma_z += v[2]  # Soma Z
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

        self.ka = [ka[0], ka[1], ka[2]]  # (r, g, b)
        self.kd = [kd[0], kd[1], kd[2]]
        self.ks = [ks[0], ks[1], ks[2], ks[3]]  # (r, g, b, n)

        x, y, z = v0[0], v0[1], v0[2]
        l = lado

        # não sofre transformações
        v0 = (x, y, z, 1)  # Trás-Esq-Baixo
        v1 = (x + l, y, z, 1)  # Trás-Dir-Baixo
        v2 = (x, y + l, z, 1)  # Trás-Esq-Cima
        v3 = (x + l, y + l, z, 1)  # Trás-Dir-Cima)
        v4 = (x, y, z + l, 1)  # Frente-Esq-Baixo
        v5 = (x + l, y, z + l, 1)  # Frente-Dir-Baixo
        v6 = (x, y + l, z + l, 1)  # Frente-Esq-Cima
        v7 = (x + l, y + l, z + l, 1)  # Frente-Dir-Cima

        self.vertices_modelo = [v0, v1, v2, v3, v4, v5, v6, v7]
        self.vertices_modelo_transformados = list(self.vertices_modelo)

        # Faces em sentido anti-horário
        face0 = Face(4, 5, 7, 6)  # Frente
        face1 = Face(1, 0, 2, 3)  # Traś
        face2 = Face(0, 4, 6, 2)  # Direita
        face3 = Face(5, 1, 3, 7)  # Esquerda
        face4 = Face(2, 6, 7, 3)  # Topo
        face5 = Face(4, 0, 1, 5)  # Base

        self.lista_faces = (face0, face1, face2, face3, face4, face5)

        # faces que vão sofrer alterações
        self.model_faces = [face0, face1, face2, face3, face4, face5]
        # Dados do mundo

        # matrix que vai sofrer transformações e ser rasterizada

        self.rotacao = [0.0, 0.0, 0.0]  # Rotação atual
        self.escala = 1.0  # escala atual
        self.atualizar_normais()
        self.centroide = self.calcular_centroide()

        self.trans = [
            self.centroide[0],
            self.centroide[1],
            self.centroide[2],
        ]  # Posição atual (referência no centróide)


class Camera:

    def get_view_spec(self):
        return (self.u, self.v, self.n)

    def cal_view_spec(self):
        # função para calcular o view spec (página 4 do artigo do Alvy-Ray)

        n = Vector.normalize(self.N)

        up = Vector.normalize(self.Y)

        dot = Vector.dot_product(up, n)

        vx = up[0] - (dot * n[0])
        vy = up[1] - (dot * n[1])
        vz = up[2] - (dot * n[2])

        v_temp = [vx, vy, vz]
        v = Vector.normalize(v_temp)

        # calcular vetor u (invertido pra usar a regra da mão direita)
        u = Vector.normalize(Vector.cross_product(n, v))

        return u, v, n

    def __init__(
        self,
        vrp,
        prp,
        vpn,
        vup,
        P,
        Y,
        u_max,
        u_min,
        v_max,
        v_min,
        DP,
        near,
        far,
        Vres,
        Hres,
    ):

        self.vrp = [vrp[0], vrp[1], vrp[2]]
        self.vpn = [vpn[0], vpn[1], vpn[2]]
        self.vup = [vup[0], vup[1], vpn[2]]

        self.prp = [prp[0], prp[1], prp[2]]

        self.N = Vector.create_vector(vrp, P)

        self.Y = [Y[0], Y[1], Y[2]]

        self.u, self.v, self.n = self.cal_view_spec()

        # Distância focal (d)
        self.DP = DP

        self.z_min = near / far
        self.z_max = 1
        self.Vres = Vres
        self.Hres = Hres

        self.window = {"u_min": u_min, "u_max": u_max, "v_min": v_min, "v_max": v_max}

        self.Cu = (self.window["u_max"] + self.window["u_min"]) / 2
        self.Cv = (self.window["v_max"] + self.window["v_min"]) / 2
        self.Su = (self.window["u_max"] - self.window["u_min"]) / 2
        self.Sv = (self.window["v_max"] - self.window["v_min"]) / 2
        self.AR = self.Su / self.Sv
        self.PAR = self.AR * (self.Vres / self.Hres)

        # Planos de Recorte (Clipping) para definir o Volume de Visão
        self.near = near  # Distância mínima (Z min)
        self.far = far  # Distância máxima (Z max)


class RenderPoligon:
    # classe para definir o polígono renderizavel, guardando vertices do cubo após recorte
    # evitar mudar a classe cubo, pra não afetar o trabalho dos outros
    # representa uma face, que é a unidade basica a ser renderizada
    def __init__(self, vertices_2d, ka, kd, ks, normal):
        self.vertices_2d = vertices_2d
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.normal = normal


class Luz:
    # Constantes para legibilidade
    PONTUAL = 1  # fonte de luz na cena
    DIRECIONAL = 2  # fonte de luz no infinito

    def __init__(self, tipo, vetor_pos_dir, intensidade_rgb_s, intensidade_rgb_d):
        self.tipo = tipo  # Luz.PONTUAL ou Luz.DIRECIONAL

        # Se for PONTUAL, vetor_pos_dir é a Posição (x, y, z)
        # Se for DIRECIONAL, vetor_pos_dir é a Direção (dx, dy, dz)
        self.posicao_ou_direcao = [vetor_pos_dir[0], vetor_pos_dir[1], vetor_pos_dir[2]]

        # Intensidades da Fonte Luminosa
        # Cor da luz
        self.id = [
            intensidade_rgb_d[0],
            intensidade_rgb_d[1],
            intensidade_rgb_d[2],
        ]  # Intensidade Difusa (RGB)
        self.i_spec = [
            intensidade_rgb_s[0],
            intensidade_rgb_s[1],
            intensidade_rgb_s[2],
        ]  # Intensidade Especular (Geralmente igual à difusa)


class Cena:
    def __init__(self, height, width):
        # --- Gerenciamento de Objetos ---
        self.objetos = []  # Lista de instâncias de Cubo
        self.luzes = []  # Lista de instâncias de Luz
        self.camera = None  # Instância de Camera
        self.height = height
        self.width = width

        self.viewport = {"x_min": 0, "y_min": 0, "x_max": width, "y_max": height}

        # Luz Ambiente Global (Ilumina todas as faces minimamente)
        self.ia = [0.1, 0.1, 0.1]  # Cinza escuro fraco

        # Modo de shader para renderização
        self.modo_shader = 2  # 1 = Flat, 2 = Phong

        # --- Buffers de Rasterização (Alocação de Memória) ---
        # ColorBuffer: Matriz width x height guardando tuplas (R, G, B)
        # Uma entrada para cada pixel
        # Inicializa tudo com preto (0,0,0)
        self.color_buffer = [[(0, 0, 0) for _ in range(height)] for _ in range(width)]

        # DepthBuffer (Z-Buffer): Matriz width x height guardando floats
        # Inicializa com infinito positivo (qualquer objeto será menor que infinito)
        self.depth_buffer = [
            [float("inf") for _ in range(height)] for _ in range(width)
        ]

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
                self.color_buffer[x][y] = [0, 0, 0]  # Cor de fundo
                self.depth_buffer[x][y] = float("inf")

    @staticmethod
    def inserir_vertice_ordenado(p_inicio, p_fim, novo_vertice):
        atual = p_inicio
        # Procura a posição correta baseada no 'alpha' (distância do início da reta)
        while atual.proximo != p_fim and atual.proximo.alpha < novo_vertice.alpha:
            atual = atual.proximo

        # Insere o novo_vertice na corrente
        novo_vertice.proximo = atual.proximo
        atual.proximo = novo_vertice

    def _dentro_plano(self, v, plano):
        """
        Verifica se um vértice (x, y, z, w) está dentro do semi-espaço definido pelo plano.
        Plano = (A, B, C, D) tal que Ax + By + Cz + Dw >= 0 é 'dentro'.
        """
        # Produto escalar 4D: v . plano
        dot = (v[0] * plano[0]) + (v[1] * plano[1]) + (v[2] * plano[2]) + (v[3] * plano[3])
        # Usamos um epsilon negativo pequeno para tolerância
        return dot >= -1e-5

    def _intersecao_plano(self, anterior, atual, plano):
        """
        Calcula o vértice de interseção entre a aresta (anterior->atual) e o plano.
        Retorna (ix, iy, iz, iw, inormal) interpolado.
        """
        # Distâncias dos pontos ao plano (produto escalar)
        dist_ant = (anterior[0] * plano[0]) + (anterior[1] * plano[1]) + (anterior[2] * plano[2]) + (anterior[3] * plano[3])
        dist_atu = (atual[0] * plano[0]) + (atual[1] * plano[1]) + (atual[2] * plano[2]) + (atual[3] * plano[3])

        # Fator t (0.0 a 1.0) onde a interseção ocorre
        # t = dist_ant / (dist_ant - dist_atu)
        denominador = dist_ant - dist_atu
        if abs(denominador) < 1e-6:
            return atual # Evita divisão por zero, retorna o ponto atual

        t = dist_ant / denominador

        # Interpolação Linear (LERP) de x, y, z, w
        ix = anterior[0] + t * (atual[0] - anterior[0])
        iy = anterior[1] + t * (atual[1] - anterior[1])
        iz = anterior[2] + t * (atual[2] - anterior[2])
        iw = anterior[3] + t * (atual[3] - anterior[3])

        # Interpolação da Normal (se existir)
        inormal = None
        if len(anterior) > 4 and anterior[4] is not None and atual[4] is not None:
            n1 = anterior[4]
            n2 = atual[4]
            nx = n1[0] + t * (n2[0] - n1[0])
            ny = n1[1] + t * (n2[1] - n1[1])
            nz = n1[2] + t * (n2[2] - n1[2])
            inormal = (nx, ny, nz) # Não precisa normalizar agora, faremos no pixel shader

        return (ix, iy, iz, iw, inormal)

    def recorteSH(self, vertices_clip):
        """
        Algoritmo Sutherland-Hodgman 3D (Clip Space).
        Recebe lista de vértices [(x, y, z, w, normal), ...].
        Retorna lista recortada.
        """
        # Lista de planos de recorte no Clip Space (Ax + By + Cz + Dw = 0)
        # O mais importante para evitar explosão é o NEAR PLANE.
        # Na maioria das projeções: z + w >= 0 ou z >= -w
        # Plano Near: (0, 0, 1, 1) -> 0x + 0y + 1z + 1w >= 0
        
        # Você pode adicionar os outros planos (laterais) aqui se quiser um recorte completo
        planos = [
            (0, 0, 1, 1),    # Near Plane (Corta o que está atrás da câmera)
            (0, 0, -1, 1), # Far Plane (opcional)
            (1, 0, 0, 1),  # Left Plane (opcional)
            (-1, 0, 0, 1), # Right Plane (opcional)
            (0, 1, 0, 1),  # Bottom Plane (opcional)
            (0, -1, 0, 1)  # Top Plane (opcional)
        ]

        output_list = vertices_clip

        for plano in planos:
            input_list = output_list
            output_list = []
            
            if not input_list:
                break

            for i in range(len(input_list)):
                atual = input_list[i]
                anterior = input_list[(i - 1) % len(input_list)] # Pega o anterior (cíclico)

                atual_dentro = self._dentro_plano(atual, plano)
                anterior_dentro = self._dentro_plano(anterior, plano)

                if atual_dentro:
                    if not anterior_dentro:
                        # Saiu -> Entrou: Adiciona interseção E o atual
                        interseccao = self._intersecao_plano(anterior, atual, plano)
                        output_list.append(interseccao)
                    
                    # Entrou -> Entrou (ou Saiu -> Entrou): Adiciona o atual
                    output_list.append(atual)
                
                elif anterior_dentro:
                    # Entrou -> Saiu: Adiciona SOMENTE interseção
                    interseccao = self._intersecao_plano(anterior, atual, plano)
                    output_list.append(interseccao)
                
                # Se (não atual_dentro) e (não anterior_dentro): não faz nada (rejeita)

        return output_list


    def _rasterizar_face(
        self, vertices_tela, shader_mode, cor_flat=None, material=None
    ):
        """
        shader_mode: 1 = Flat (Constante); 2 = Phong
        cor_flat: Tupla (r, g, b) já calculada (para o Flat)
        material: Objeto com ka, kd, ks (para o Phong)
        """

        # 1. Encontrar limites em Y
        y_min = int(min(v.y for v in vertices_tela))
        y_max = int(max(v.y for v in vertices_tela))

        # Clipagem básica da tela em Y
        y_min = max(0, y_min)
        y_max = min(self.height, y_max)

        # Tabela de arestas (ET)
        et = {y: [] for y in range(y_min, y_max)}
        n = len(vertices_tela)

        for i in range(n):
            p1 = vertices_tela[i]
            p2 = vertices_tela[(i + 1) % n]

            # Ordenar p1 (menor Y) -> p2 (maior Y)
            if p1.y > p2.y:
                p1, p2 = p2, p1

            dy = p2.y - p1.y
            if dy == 0:
                continue  # Ignora arestas horizontais

            dx_dy = (p2.x - p1.x) / dy
            dz_dy = (p2.z - p1.z) / dy

            start_y = int(math.ceil(p1.y))  # Próxima scanline válida
            offset_y = start_y - p1.y

            aresta = {
                "ymax": int(math.ceil(p2.y)),
                "x": p1.x + (offset_y * dx_dy),  # Ajuste sub-pixel
                "dx_dy": dx_dy,
                "z": p1.z + (offset_y * dz_dy),  # Ajuste sub-pixel
                "dz_dy": dz_dy,
            }

            # Dados básicos da aresta
            # aresta = {
            #    "ymax": p2.y,
            #    "x": p1.x,
            #    "dx_dy": dx_dy,
            #    "z": p1.z,
            #    "dz_dy": dz_dy,
            # }

            # Para o Phong, interpolamos as normais
            if shader_mode == 2:
                dnx_dy = (p2.normal[0] - p1.normal[0]) / dy
                dny_dy = (p2.normal[1] - p1.normal[1]) / dy
                dnz_dy = (p2.normal[2] - p1.normal[2]) / dy

                aresta.update(
                    {
                        "nx": p1.normal[0],
                        "dnx_dy": dnx_dy,
                        "ny": p1.normal[1],
                        "dny_dy": dny_dy,
                        "nz": p1.normal[2],
                        "dnz_dy": dnz_dy,
                    }
                )

            # start_y = int(p1.y)
            if start_y < y_max:
                if start_y < 0:
                    start_y = 0  # Clipagem simples superior
                if start_y in et:
                    et[start_y].append(aresta)

        # Lista de arestas ativas (AET)
        aet = []

        # 2. Varredura das scanlines
        for y in range(y_min, y_max):
            if y in et:
                aet.extend(et[y])

            # Remove as arestas concluídas
            aet = [e for e in aet if y < e["ymax"]]

            # Ordena por X
            aet.sort(key=lambda k: k["x"])

            # Preenche spans (pares de arestas)
            for i in range(0, len(aet), 2):
                if i + 1 >= len(aet):
                    break
                e1, e2 = aet[i], aet[i + 1]

                x_start = int(math.ceil(e1["x"]))
                x_end = int(math.ceil(e2["x"]))

                #   x_start = int(e1["x"] + 0.5)
                #  x_end = int(e2["x"] + 0.5)

                # Clipagem horizontal de X
                x_start = max(0, x_start)
                x_end = min(self.width, x_end)

                if x_end <= x_start:
                    continue

                span = e2["x"] - e1["x"]
                if span == 0:
                    span = 1

                # Setup de interpolação do Z
                z = e1["z"]
                dz_dx = (e2["z"] - e1["z"]) / span

                # Setup de interpolação das normais (Phong)
                if shader_mode == 2:
                    nx, ny, nz = e1["nx"], e1["ny"], e1["nz"]
                    dnx_dx = (e2["nx"] - e1["nx"]) / span
                    dny_dx = (e2["ny"] - e1["ny"]) / span
                    dnz_dx = (e2["nz"] - e1["nz"]) / span

                # 3. Loop dos Pixels (X)
                for x in range(x_start, x_end):
                    # Teste de Z-Buffer
                    # if z < self.depth_buffer[x][y]:
                    if z <= self.depth_buffer[x][y] + 1e-6:
                        self.depth_buffer[x][y] = z  # Atualiza Z

                        cor_final = (0, 0, 0)

                        if shader_mode == 1:
                            cor_final = cor_flat

                        elif shader_mode == 2:
                            # Renormalizar vetor interpolado
                            mod = math.sqrt(nx**2 + ny**2 + nz**2)
                            if mod == 0:
                                mod = 1
                            N = (nx / mod, ny / mod, nz / mod)

                            # Calcula iluminação por pixel
                            cor_final = self._calcular_phong_pixel(N, material)

                        self.color_buffer[x][y] = cor_final

                    # Incrementa Z e as normais
                    z += dz_dx
                    if shader_mode == 2:
                        nx += dnx_dx
                        ny += dny_dx
                        nz += dnz_dx

            for e in aet:
                e["x"] += e["dx_dy"]
                e["z"] += e["dz_dy"]
                if shader_mode == 2:
                    e["nx"] += e["dnx_dy"]
                    e["ny"] += e["dny_dy"]
                    e["nz"] += e["dnz_dy"]

    def _calcular_phong_pixel(self, N, material):
        # N -> vetor normal interpolado

        # 1. Componente ambiente (Ia * Ka)
        # Inicia com cor ambiente global
        r = self.ia[0] * material.ka[0]
        g = self.ia[1] * material.ka[1]
        b = self.ia[2] * material.ka[2]

        # Posição do observador (assumindo que está em +Z infinito para simplificar)
        S = self.camera.vrp
        #S = (0, 0, 1)

        for luz in self.luzes:
            # Recupera direção da luz (considerando como direcional)
            # L é vetor contrário da direção da luz
            lx, ly, lz = (
                luz.posicao_ou_direcao[0],
                luz.posicao_ou_direcao[1],
                luz.posicao_ou_direcao[2],
            )

            # Normaliza L
            mod_l = math.sqrt(lx**2 + ly**2 + lz**2)
            if mod_l == 0:
                mod_l = 1

            L = (lx / mod_l, ly / mod_l, lz / mod_l)

            # 2. Componente difusa (Id * Kd * (N * L))
            dot_nl = max(0, N[0] * L[0] + N[1] * L[1] + N[2] * L[2])

            r += luz.id[0] * material.kd[0] * dot_nl
            g += luz.id[1] * material.kd[1] * dot_nl
            b += luz.id[2] * material.kd[2] * dot_nl

            # 3. Componente especular simplificado (Is * Ks * (N * H)^n)
            if dot_nl > 0:  # Só existe especular se a luz atinge a face

                # Estamos calculando o H dentro do loop para deixar a possibilidade de usar
                # iluminação pontual ou câmeras móveis no projeto e a diferença de performance é mínima

                # Cálculo do vetor H (Halfway/Bissetriz)
                # H = (L + S) / |L + S|
                hx = L[0] + S[0]
                hy = L[1] + S[1]
                hz = L[2] + S[2]

                mod_h = math.sqrt(hx**2 + hy**2 + hz**2)
                if mod_h == 0:
                    mod_h = 1
                H = (hx / mod_h, hy / mod_h, hz / mod_h)

                # Produto escalar (N * H)
                dot_nh = max(0, N[0] * H[0] + N[1] * H[1] + N[2] * H[2])

                # Expoente especular (brilho)
                spec = dot_nh ** material.ks[3]

                r += luz.i_spec[0] * material.ks[0] * spec
                g += luz.i_spec[1] * material.ks[1] * spec
                b += luz.i_spec[2] * material.ks[2] * spec

        # Clamp para garantir RGB entre 0 e 255
        r = min(255, max(0, int(r * 255)))
        g = min(255, max(0, int(g * 255)))
        b = min(255, max(0, int(b * 255)))

        return (r, g, b)

    def renderizar(self):
        self.limpar_buffers()

        if not self.camera:
            print("Câmera não instânciada")
            return

        # 1. PEGAR MATRIZES DE PROJEÇÃO E TELA (Usando o Pipeline do logica.py)
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
            self.viewport["x_max"],
            self.viewport["x_min"],
            self.viewport["y_max"],
            self.viewport["y_min"],
            self.camera.z_max,
            self.camera.z_min,
        )
        mat_M = Pipeline.get_matrix_M()

        # Composição: Mundo -> Clip Space -> Tela
        m_view = Mat4.mul(mat_B, mat_A)
        m_proj = Mat4.mul(mat_P, Mat4.mul(mat_D, mat_C))
        m_total_proj = Mat4.mul(m_proj, m_view)
        m_screen = Mat4.mul(mat_M, Mat4.mul(mat_L, Mat4.mul(mat_K, mat_J)))

        # 2. PROCESSAR OBJETOS
        for obj in self.objetos:
            for face in obj.lista_faces:

                # --- BACK-FACE CULLING (Remoção de Faces Ocultas) ---
                v0 = obj.vertices_modelo_transformados[face.indices[0]]
                vx = self.camera.vrp[0] - v0[0]
                vy = self.camera.vrp[1] - v0[1]
                vz = self.camera.vrp[2] - v0[2]

                # Produto Escalar (Normal da Face . Vetor Visão)
                dot_vis = (
                    (face.normal[0] * vx)
                    + (face.normal[1] * vy)
                    + (face.normal[2] * vz)
                )

                # Se a face estiver visível:
                if dot_vis > 0:

                # A. PREPARAÇÃO PARA CLIP SPACE (SEM DIVISÃO AINDA)
                    vertices_clip_space = []
                    
                    for idx in face.indices:
                        v_mundo = obj.vertices_modelo_transformados[idx]
                        # Transformação total até Clip Space
                        v_clip = Vector.mul(m_total_proj, v_mundo) 
                        
                        # Normal do vértice (para passar pelo pipeline)
                        normal_vert = obj.normais_vertices[idx]
                        
                        # Guardamos (x, y, z, w, normal)
                        vertices_clip_space.append(
                            (v_clip[0], v_clip[1], v_clip[2], v_clip[3], normal_vert)
                        )


                    #B. Recorte 3D (Sutherland-Hodgeman)
                    poly_clipado = self.recorteSH(vertices_clip_space)
                    # Se o polígono foi totalmente cortado, ignoramos
                    if len(poly_clipado) < 3:
                        continue
                    # C. DIVISÃO PERSPECTIVA E VIEWPORT
                    vertices_tela_brutos = []
                
                    for v in poly_clipado:
                        x, y, z, w, normal = v
                        
                        # Segurança extra: se w for muito pequeno (quase zero), travamos
                        if w < 0.001: w = 0.001 
                        
                        # Divisão Perspectiva (Agora segura!)
                        v_ndc = [x / w, y / w, z / w, 1.0]
                        
                        # Transformação de Viewport (NDC -> Tela)
                        v_tela = Vector.mul(m_screen, v_ndc)
                        
                        # Adiciona na lista para o Weiler-Atherton (que fará apenas ajuste fino 2D)
                        vertices_tela_brutos.append(
                            (v_tela[0], v_tela[1], v_tela[2], normal)
                        )

                    modo_shader = self.modo_shader  # 1 = Flat, 2 = Phong
                    poligonos_recortados = [vertices_tela_brutos]
                    for poligono in poligonos_recortados:
                        # O recorteWA devolve pontos 2D (x,y). Precisamos trazer o Z para o buffer.
                        # Assumimos o Z do primeiro vértice para a face 2D recortada.
                        z_base = vertices_tela_brutos[0][2]

                        vertices_prontos = []
                        for pt in poligono:
                            # pt[3] contém a normal interpolada do vértice
                            normal_interp = pt[3] if len(pt) > 3 and pt[3] is not None else face.normal
                            vertices_prontos.append(
                                VerticeTela(pt[0], pt[1], pt[2], normal=normal_interp)
                            )

                        # D. ILUMINAÇÃO (Cálculo da Cor)
                        cor_flat = (0, 0, 0)
                        if modo_shader == 1 and len(self.luzes) > 0:
                            # Flat: calcula cor uma vez usando normal da face
                            cor_flat = self._calcular_phong_pixel(face.normal, obj)
                        elif modo_shader == 1:
                            cor_flat = (100, 100, 100)  # Flat sem luz

                        # E. RASTERIZAÇÃO (SCANLINE)
                        self._rasterizar_face(
                            vertices_prontos, modo_shader, cor_flat, obj
                        )
