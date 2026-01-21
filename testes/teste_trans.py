
from src.logica import Cubo, Mat4

cubo = Cubo((0, 0, 0), 1, (1,1,1), (1,1,1), (1,1,1,10))

print("========== Cubo original ==========")
cubo.print_vertices()
print("====================")

T = Mat4.trans(2, 0, 0)
cubo.aplicar_transformacao(T)


print("========== Cubo após translação (x) ==========")
cubo.print_vertices()
print("====================")

T = Mat4.trans(-2, 0, 0)
cubo.aplicar_transformacao(T)

print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")

T = Mat4.trans(0, 2, 0)
cubo.aplicar_transformacao(T)
print("========== Cubo após translação (y) ==========")
cubo.print_vertices()
print("====================")

T = Mat4.trans(0, -2, 0)
cubo.aplicar_transformacao(T)

print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")

T = Mat4.trans(0, 0, 2)
cubo.aplicar_transformacao(T)
print("========== Cubo após translação (z) ==========")
cubo.print_vertices()
print("====================")

T = Mat4.trans(0, 0, -2)
cubo.aplicar_transformacao(T)

print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")


R = Mat4.rotate_x(45)
cubo.aplicar_transformacao(R)
print("========== Cubo após rotação (x) ==========")
cubo.print_vertices()
print("====================")



R = Mat4.rotate_x(-45)
cubo.aplicar_transformacao(R)
print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")




R = Mat4.rotate_y(45)
cubo.aplicar_transformacao(R)
print("========== Cubo após rotação (y) ==========")
cubo.print_vertices()
print("====================")



R = Mat4.rotate_y(-45)
cubo.aplicar_transformacao(R)
print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")

R = Mat4.rotate_z(45)
cubo.aplicar_transformacao(R)
print("========== Cubo após rotação (z) ==========")
cubo.print_vertices()
print("====================")



R = Mat4.rotate_z(-45)
cubo.aplicar_transformacao(R)
print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")



S = Mat4.scale(2, 1, 1)

cubo.aplicar_transformacao(S)
print("========== Cubo após escala(x) ==========")
cubo.print_vertices()
print("====================")

R = Mat4.scale(0.5,1,1)

cubo.aplicar_transformacao(R)
print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")


S = Mat4.scale(1, 2, 1)

cubo.aplicar_transformacao(S)
print("========== Cubo após escala(y) ==========")
cubo.print_vertices()
print("====================")

R = Mat4.scale(1,0.5,1)

cubo.aplicar_transformacao(R)
print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")

S = Mat4.scale(1, 1, 2)

cubo.aplicar_transformacao(S)
print("========== Cubo após escala(z) ==========")
cubo.print_vertices()
print("====================")

R = Mat4.scale(1, 1, 0.5)

cubo.aplicar_transformacao(R)
print("========== Cubo revertido  ==========")
cubo.print_vertices()
print("====================")




T = Mat4.trans(2, 0, 0)
R = Mat4.rotate_y(45)
S = Mat4.scale(2, 2, 2)

M = Mat4.mul(T, Mat4.mul(R, S))

print("========== Teste matriz composta  ==========")
Mat4.print_matrix(M)
print("====================")

