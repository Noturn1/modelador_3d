# Se o arquivo logica.py estiver na mesma pasta, use:
from src import Cena, Cubo, Camera, Luz, Mat4
from PIL import Image

def executar_teste_renderizacao():
    print("=== Iniciando Teste de Renderização 3D ===")

    # 1. Configuração da Tela (100x100)
    largura, altura = 1600, 900
    cena = Cena(altura, largura)

    # 2. Criar um Cubo Menor (Lado 10) para evitar clipping excessivo
    # v0 (origem), lado, ka, kd, ks
    #  ka, kd, ks = [0.2, 0.2, 0.2], [0.7, 0.7, 0.7], [1.0, 1.0, 1.0, 30]
    
    # Centralizamos o cubo criando-o em [-5, -5, -5]
    lado_cubo = 20
    cubo = Cubo([0, 0, 0], lado_cubo, [0.2, 0.2, 0.2], [0.8, 0.8, 0.8], [1.0, 1.0, 1.0, 50])

    
    # Aplicar rotação para ver as faces superior, frontal e lateral
    mat_transform = Mat4.mul(Mat4.rotate_x(45, cubo.centroide), Mat4.rotate_y(0, cubo.centroide))
    mat_transform = Mat4.mul(mat_transform,Mat4.trans(-cubo.centroide[0], -cubo.centroide[1], -cubo.centroide[2]))
    cubo.aplicar_transformacao(mat_transform)
    
    cena.adicionar_objeto(cubo)

    cam = Camera(
        vrp=[0, 0, -40],  # Ponto de observação (octante negativo)
        prp=[0, 0, 0],
        vpn=[0, 0, 1],
        vup=[0, 1, 0],
        P=[0, 0, 0],       # Alvo: Centro do cubo para mantê-lo centralizado
        Y=[0, 1, 0],
        # Janela apertada (-15 a 15) para o cubo de lado 20 parecer "grande"
        u_min=-15, u_max=15, 
        v_min=-15, v_max=15, 
        DP=20,                # Distância Focal (Zoom)
        near=1, far=200,
        Vres=altura, Hres=largura
    )
    cena.definir_camera(cam)
    # 4. Adicionar Luz para testar o Shading de Phong
    luz = Luz(Luz.DIRECIONAL, [1, 1, 1], [1, 1, 1], [1, 1, 1])
    cena.adicionar_luz(luz)
    # 5. Renderizar
    print("Renderizando frame...")
    cena.renderizar()

    # 6. Analisar Color Buffer
    pixels_coloridos = 0
    cores_encontradas = set()

    for x in range(largura):
        for y in range(altura):
            cor = cena.color_buffer[x][y]
            if cor != (0, 0, 0) and cor != [0, 0, 0]:
                pixels_coloridos += 1
                cores_encontradas.add(cor)

    print("-" * 40)
    if pixels_coloridos > 0:
        print(f"SUCESSO! Pixels desenhados: {pixels_coloridos}")
        print(f"Diferentes tons de cor detectados: {len(cores_encontradas)} (Indica iluminação ativa)")
    else:
        print("ERRO: A tela continua preta.")
        print("Dica: Verifique se você corrigiu a linha 761 do logica.py (y_min vs y_max).")
    print("-" * 40)

    if pixels_coloridos > 0:
        print(f"SUCESSO! Pixels desenhados: {pixels_coloridos}")
        # Chamar a nova função
        exportar_para_imagem(cena, "cubo_renderizado.png")
    else:
        print("FALHA: Nada foi desenhado.")

def exportar_para_imagem(cena, nome_arquivo="resultado.png"):
    """
    Converte o color_buffer da Cena em um arquivo de imagem.
    """
    # 1. Criar uma nova imagem RGB com as dimensões da cena
    # O Pillow usa (width, height)
    img = Image.new("RGB", (cena.width, cena.height))
    pixels = img.load()

    # 2. Percorrer o buffer e preencher a imagem
    for x in range(cena.width):
        for y in range(cena.height):
            # O color_buffer armazena (r, g, b)
            cor = cena.color_buffer[x][y]
            
            # Garantir que a cor seja uma tupla de inteiros
            # Invertemos o Y no preenchimento caso a imagem saia de ponta-cabeça
            pixels[x, (cena.height - 1) - y] = tuple(map(int, cor))

    # 3. Salvar o arquivo
    img.save(nome_arquivo)
    print(f"Imagem exportada com sucesso: {nome_arquivo}")



if __name__ == "__main__":
    executar_teste_renderizacao()