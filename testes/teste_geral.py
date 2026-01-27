from src.logica import Cena, Cubo, Camera, Luz, Mat4

def testar_pipeline_grafico():
    print("Iniciando teste do Pipeline Gráfico...")

    # 1. Configuração da Cena (Resolução 100x100 para teste rápido)
    largura, altura = 100, 100
    cena = Cena(altura, largura)

    # 2. Criar um Cubo
    # v0 (pos), lado, ka, kd, ks (cor branca com brilho)
    ka = [0.2, 0.2, 0.2]
    kd = [0.8, 0.8, 0.8]
    ks = [1.0, 1.0, 1.0, 50] # RGB + Brilho (n=50)
    cubo = Cubo([0, 0, 0], 30, ka, kd, ks)
    
    # Aplicar uma rotação para vermos mais de uma face
    mat_rot = Mat4.rotate_y(45)
    mat_rot = Mat4.mul(Mat4.rotate_x(30), mat_rot)
    cubo.aplicar_transformacao(mat_rot)
    
    cena.adicionar_objeto(cubo)

    # 3. Configurar a Câmera
    # vrp, prp, vpn, vup, P (alvo), Y (direção up), janela, dist_focal, planos_corte, resolução
    cam = Camera(
        vrp=[0, 0, 50],   # Câmera afastada no eixo Z
        prp=[0, 0, 0],
        vpn=[0, 0, 1],
        vup=[0, 1, 0],
        P=[0, 0, 0],      # Olhando para a origem
        Y=[0, 1, 0],
        u_min=-10, u_max=10, v_min=-10, v_max=10,
        DP=20,            # Distância Focal
        near=1, far=100,
        Vres=altura, Hres=largura
    )
    cena.definir_camera(cam)

    # 4. Adicionar uma Luz Direcional
    # Tipo, Direção, Intensidade Specular, Intensidade Difusa
    luz = Luz(Luz.DIRECIONAL, [1, -1, -1], [1, 1, 1], [1, 1, 1])
    cena.adicionar_luz(luz)

    # 5. Executar Renderização
    print("Executando renderizar()...")
    cena.renderizar()

    # 6. Verificação de Resultados
    pixels_desenhados = 0
    for x in range(largura):
        for y in range(altura):
            if cena.color_buffer[x][y] != [0, 0, 0]:
                pixels_desenhados += 1

    print("-" * 30)
    if pixels_desenhados > 0:
        print(f"SUCESSO: O cubo foi rasterizado!")
        print(f"Total de pixels coloridos: {pixels_desenhados}")
        # Exemplo de cor de um pixel central
        print(f"Cor no centro (50,50): {cena.color_buffer[50][50]}")
    else:
        print("FALHA: Nada foi desenhado (Tela Preta). Verifique a posição da câmera ou o Back-face Culling.")
    print("-" * 30)

if __name__ == "__main__":
    testar_pipeline_grafico()
