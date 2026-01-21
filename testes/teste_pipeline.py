from src.logica import (
    Cubo, Camera, Pipeline, Mat4, Vector
)

# =========================================================
# 1. Criar objeto no mundo
# =========================================================

cubo = Cubo(
    v0=(0, 0, 0),
    lado=1,
    ka=(1,1,1),
    kd=(1,1,1),
    ks=(1,1,1,10)
)

print("========== Vértices do cubo (MODEL SPACE) ==========")
cubo.print_vertices()
print("===================================================\n")

# =========================================================
# 2. Criar câmera (Alvy-Ray Smith)
# =========================================================

camera = Camera(
    vrp=(30, 40, 100),   # posição da câmera
    vpn=(1, 2, 1),  # direção de visão
    vup=(0, 1, 0),    # vetor up
    prp = (1, 0, 0),
    near = 0,
    far = 100,
    d = 1,
    u_min = -1,
    u_max = 1,
    v_min = -1,
    v_max = 1,
)

u, v, n = camera.u, camera.v, camera.n

print("View Spec (u, v, n):")
print("u =", u)
print("v =", v)
print("n =", n)
print()

# =========================================================
# 3. Construção das matrizes do pipeline
# =========================================================

# --- Matriz A (translação do VRP) ---
A = Pipeline.get_matrix_A(camera.vrp)

# --- Matriz B (orientação da câmera) ---
B = Pipeline.get_matrix_B(u, v, n)

# --- Parâmetros da janela ---
Cu = (camera.window["u_max"] + camera.window["u_min"]) / 2
Cv = (camera.window["v_max"] + camera.window["v_min"]) / 2
Su = (camera.window["u_max"] - camera.window["u_min"])
Sv = (camera.window["v_max"] - camera.window["v_min"])

d = camera.distancia_focal
f = camera.far
zmin = camera.near

C = Pipeline.get_matrix_C(Cu, Cv, d)
D = Pipeline.get_matrix_D(Su, Sv, d, f)
P = Pipeline.get_matrix_P(zmin)
J = Pipeline.get_matrix_J()
K = Pipeline.get_matrix_K()

# Viewport fictício (0..800, 0..600)
L = Pipeline.get_matrix_L(
    x_max=800, x_min=0,
    y_max=600, y_min=0,
    z_max=1,   z_min=0
)

Mvp = Pipeline.get_matrix_M()

# =========================================================
# 4. Composição da MATRIZ FINAL do pipeline
# =========================================================

# Ordem: M = Mvp * L * K * J * P * D * C * B * A
M_pipeline = Mat4.mul(
    Mvp,
    Mat4.mul(
        L,
        Mat4.mul(
            K,
            Mat4.mul(
                J,
                Mat4.mul(
                    P,
                    Mat4.mul(
                        D,
                        Mat4.mul(
                            C,
                            Mat4.mul(B, A)
                        )
                    )
                )
            )
        )
    )
)

print("========== MATRIZ FINAL DO PIPELINE ==========")
Mat4.print_matrix(M_pipeline)
print("==============================================\n")

# =========================================================
# 5. Aplicar pipeline a UM vértice (teste unitário)
# =========================================================

v_model = cubo.vertices_modelo_transformados[0]
v_clip = Vector.mul(M_pipeline, v_model)

print("Vértice original (MODEL):", v_model)
print("Após pipeline completo :", v_clip)

# Normalização homogênea (NDC)
if v_clip[3] != 0:
    v_ndc = (
        v_clip[0] / v_clip[3],
        v_clip[1] / v_clip[3],
        v_clip[2] / v_clip[3]
    )
    print("Após divisão por W (NDC):", v_ndc)

print("\n========== FIM DO TESTE DO PIPELINE ==========")

