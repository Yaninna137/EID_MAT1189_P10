import sympy as sp
import numpy as np

class ModeloCosto:
    def __init__(self, funcion_str: str):
        # x -> Porcentaje de uso CPU
        # y -> Cantidad de RAM utilizada
        # z -> Numero de procesos activos
        self.symbols = sp.symbols('x y z')

        funcion_str = funcion_str.replace('^', '**')  # Reemplaza ^ por ** para compatibilidad con sympy

        try:
            self.funcion = sp.sympify(funcion_str)
        except (sp.SympifyError, TypeError) as e:
            raise ValueError(f"Error al convertir la función: {e}, asegúrate de que la función esté en un formato válido.")
        
        if not self.funcion.free_symbols.issubset(set(self.symbols)):
            raise ValueError("La función contiene variables no permitidas. Solo se permiten x, y, z.")
        
        # Funcion
        self.funcion_lambda = sp.lambdify(self.symbols, self.funcion, 'numpy')
        
        # Curvas de nivel
        self.curvas_nivel = {}
        def calcular_curvas_nivel(self, niveles: list):
            """Calcula las curvas de nivel para los niveles especificados."""
            for nivel in niveles:
                ecuacion = sp.Eq(self.funcion, nivel)
                soluciones = sp.solve(ecuacion, self.symbols[2])  # Resuelve para z
                self.curvas_nivel[nivel] = soluciones

        # Gradiente de la función para obtener las derivadas parciales
        self.gradient = [sp.diff(self.funcion, var) for var in self.symbols]
        self.gradient_lambda = sp.lambdify(self.symbols, self.gradient, 'numpy')

        def evaluar_gradiente(self, x_val, y_val, z_val):
            """Evalúa el gradiente en un punto específico (x, y, z)."""
            return self.gradient_lambda(x_val, y_val, z_val)
        
        # Derivadas parciales
        self.dX = self.gradient[0]
        self.dY = self.gradient[1]
        self.dZ = self.gradient[2]

        # Derivadas direccionales
        def derivada_direccional(self, punto: tuple, direccion: list):
            """Calcula la derivada direccional en un punto dado y una dirección específica."""
            grad = self.evaluar_gradiente(*punto)
            direccion = np.array(direccion)
            direccion = direccion / np.linalg.norm(direccion)  # Normaliza la dirección
            return np.dot(grad, direccion)
        
        # Plano tangente
        def plano_tangente(self, punto: tuple):
            """Calcula la ecuación del plano tangente en un punto dado."""
            x0, y0, z0 = punto
            f0 = self.funcion.subs({self.symbols[0]: x0, self.symbols[1]: y0, self.symbols[2]: z0})
            grad = self.evaluar_gradiente(x0, y0, z0)
            tang = f"z - {f0} = {grad[0]}*(x - {x0}) + {grad[1]}*(y - {y0}) + {grad[2]}*(z - {z0})"
            return tang


        # Puntos críticos
        def puntos_criticos(self):
            """Encuentra los puntos críticos de la función."""
            soluciones = sp.solve(self.gradient, self.symbols)
            return soluciones

