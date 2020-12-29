import numpy as np
vec_1 = [2,4,6]
vec_2 = [1,2,3]
print(vec_1)
print(vec_2)
vec_new  = vec_1 + vec_2
print(vec_new)
vec_1 = np.array(vec_1)
print("vec_1 tiene tipo:",type(vec_1))
print(vec_1)
vec_2 = np.array(vec_2)
print("vec_2 tiene tipo:",type(vec_2))
print(vec_2)

suma = vec_1 + vec_2
print("La suma es:",suma)
resta = vec_1 - vec_2
print("La resta es:",resta)
sum_comp = np.sum(vec_1)
print("La suma de componentes es:",sum_comp)

escalar = 3
print("Escalar es:",escalar)
producto = vec_1 * escalar
print("La multiplicacion escalar de vector1:",producto)
division = vec_1 / escalar
print("La division escalar de vector1:",division)
print("La suma y resta de vector y escalar se hace con broadcasting agregando dimensiones faltantes con valor del escalar")
suma = vec_1 + escalar
print("La suma escalar es:",suma)
resta = vec_1 - escalar
print("La resta escalar es:",resta)
print("La division y multiplicacion de vectores")
producto = np.multiply(vec_1,vec_2)
print("La multiplicacion de vectores:",producto)
division = np.divide(vec_1,vec_2)
print("La division de vectores:",division)

coseno = np.dot(vec_1,vec_2) / \
       ( ( np.sqrt(np.sum(vec_1**2)) ) * ( np.sqrt(np.sum(vec_2**2)) ) )
print("Valor coseno es:",coseno)
