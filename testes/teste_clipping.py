from src.logica import Cena, Camera

# 1. Configurar uma Câmera e Cena "falsas" apenas com os dados da Tela (Viewport)
# Tela de 800x600
camera_teste = Camera(
    vrp=(0,0,0), 
    prp = (0, 0, 0),
    vpn = (0, 0, 1),
    vup = (0, 1, 0),
    P=(0,0,-1), Y=(0,1,0),
    u_max=1, u_min=-1, v_max=1, v_min=-1, 
    DP=1, 
    near=1, 
    far=10,
    Vres=600, Hres=800
)



cena = Cena(height=600, width=800)
cena.definir_camera(camera_teste)

# ==============================================================================
# TESTE 1: POLÍGONO 100% DENTRO DA TELA
# Um triângulo pequeno no meio da tela.
# ==============================================================================
print("--- TESTE 1: Polígono DENTRO da tela ---")
# Vértices (X, Y, Z) - O Z (terceiro valor) é irrelevante no 2D, pode ser 0.
triangulo_dentro = [
    (100, 100, 0), 
    (300, 100, 0), 
    (200, 300, 0)
]

resultado1 = cena.recorteWA(triangulo_dentro)
print(f"Esperado: 1 polígono igual ao original.")
print(f"Resultado: {len(resultado1)} polígono(s)")
print(resultado1)
for p in resultado1:
    print([f"({x:.1f}, {y:.1f})" for x, y in p])


# ==============================================================================
# TESTE 2: POLÍGONO CRUZANDO A BORDA SUPERIOR (Y=600)
# A ponta de cima do triângulo (400, 700) está 100 pixels fora da tela.
# ==============================================================================
print("\n--- TESTE 2: Polígono CORTANDO a borda superior ---")
triangulo_borda = [
    (200, 500, 0), # Dentro
    (600, 500, 0), # Dentro
    (400, 700, 0)  # FORA! (Y > 600)
]

resultado2 = cena.recorteWA(triangulo_borda)
print(f"Esperado: 1 polígono com 4 vértices (o topo do triângulo vira uma reta no Y=600).")
print(f"Resultado: {len(resultado2)} polígono(s)")
for p in resultado2:
    print([f"({x:.1f}, {y:.1f})" for x, y in p])


# ==============================================================================
# TESTE 3: POLÍGONO 100% FORA DA TELA
# Um quadrado na posição X=900 (A tela vai só até 800)
# ==============================================================================
print("\n--- TESTE 3: Polígono FORA da tela ---")
quadrado_fora = [
    (900, 100, 0),
    (950, 100, 0),
    (950, 150, 0),
    (900, 150, 0)
]

resultado3 = cena.recorteWA(quadrado_fora)
print(f"Esperado: 0 polígonos.")
print(f"Resultado: {len(resultado3)} polígono(s)")
