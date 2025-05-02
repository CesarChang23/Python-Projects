from scipy.optimize import linprog

# Coeficientes de la función objetivo (maximizar Z = 1000x1 + 1500x2 + 2000x3)
# Convertimos a valores negativos porque linprog minimiza por defecto
c = [-1000, -1500, -2000]

# Restricciones
# x1 + x2 + x3 <= 30 (máximo 30 productos)
# 30x1 + 60x2 + 60x3 <= 1500 (máximo 1500 pies cúbicos)
# 8000x1 + 13000x2 + 15000x3 <= 400000 (presupuesto de 400000 UM)
A = [
    [1, 1, 1],
    [30, 60, 60],
    [8000, 13000, 15000]
]

# Lado derecho de las restricciones
b = [30, 1500, 400000]

# Límites inferiores de las variables (x1, x2, x3 >= 0)
x_bounds = (0, None)  # Sin límite superior, solo inferior en 0

# Resolver el problema de optimización lineal usando HiGHS
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds, x_bounds], method='highs')

# Mostrar resultados
if result.success:
    print("Cantidad óptima de productos a exportar:")
    print(f"Producto A: {result.x[0]:.2f}")
    print(f"Producto B: {result.x[1]:.2f}")
    print(f"Producto C: {result.x[2]:.2f}")
    print(f"Beneficio máximo: {-result.fun:.2f} UM")
else:
    print("No se encontró una solución óptima.")
