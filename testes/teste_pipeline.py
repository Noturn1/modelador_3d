from src.logica import Cubo, Camera, Pipeline, Mat4, Vector

# =========================================================
# 1. Criar cubo em MODEL SPACE
# =========================================================

cubo = Cubo(
    v0=(0, 0, 0),
    lado=100,
    ka=(1, 1, 1),
    kd=(1, 1, 1),
    ks=(1, 1, 1, 10)
)

print("\n===== MODEL SPACE (CUBO) =====")
cubo.print_vertices()

# =========================================================
# 2. Criar câmera (Alvy-Ray Smith, mão direita)
# =========================================================

camera = Camera(
    vrp=(30, 40, 250),     # View Reference Point (posição da câmera)
    P=(1, 2, 1),        # Ponto observado
    Y=(0, 1, 0),        # View-Up
    u_max=400,
    u_min=-400,
    v_max=300,
    v_min=-300,
    DP=200,               # distância focal
    near=10,
    far=400,
    x_min=0,
    x_max=800,
    y_min=0,
    y_max=600,
    Vres=600,
    Hres=900
)

u, v, n = camera.get_view_spec()

print("\n===== VIEW SPEC =====")
print("u =", u)
print("v =", v)
print("n =", n)

# =========================================================
# 3. Matrizes do pipeline
# =========================================================

A = Pipeline.get_matrix_A(camera.vrp)       # Translação VRP
B = Pipeline.get_matrix_B(u, v, n)          # Orientação da câmera
C = Pipeline.get_matrix_C(camera.Cu, camera.Cv, camera.DP)
D = Pipeline.get_matrix_D(camera.Su, camera.Sv, camera.DP, camera.far)
P = Pipeline.get_matrix_P(camera.far, camera.near)

#J = Mat4.identity()
#K = Mat4.identity()
#L = Mat4.identity()

J = Pipeline.get_matrix_J()
K = Pipeline.get_matrix_K()
L = Pipeline.get_matrix_L(
    camera.viewport["x_max"],
    camera.viewport["x_min"],   
    camera.viewport["y_max"],
    camera.viewport["y_min"],
    camera.z_max,
    camera.z_min
)

#M = Mat4.identity()
M = Pipeline.get_matrix_M()

# =========================================================
# 4. Composição da matriz final do pipeline
# =========================================================
# Ordem (vetor coluna):
# Mfinal = M · L · K · J · P · D · C · B · A

list_matrizes = [A, B, C, D, P, J, K, L, M]
i = 0
for matrix in list_matrizes:
    print()
    print(i)
    Mat4.print_matrix(matrix)
    print()
    i += 1



M_pipeline = Mat4.mul(
    M,
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

print("\n===== MATRIZ FINAL DO PIPELINE =====")
Mat4.print_matrix(M_pipeline)

# =========================================================
# 5. Aplicar pipeline aos vértices do cubo
# =========================================================

print("\n===== RESULTADO DO PIPELINE =====")

for i, v_model in enumerate(cubo.vertices_modelo_transformados):
    print(f"\nV{i} MODEL :", v_model)

    v_clip = Vector.mul(M_pipeline, v_model)
    print("CLIP       :", v_clip)

    if v_clip[3] > 0:
        v_ndc = [
            v_clip[0] / v_clip[3],
            v_clip[1] / v_clip[3],
            v_clip[2] / v_clip[3]
        ]
        print("NDC        :", v_ndc)

print("\n===== TESTE DO PIPELINE FINALIZADO =====")
