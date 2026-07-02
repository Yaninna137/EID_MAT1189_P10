import streamlit as st
import plotly.graph_objects as go
import numpy as np
import re

import sympy as sp
from model.modelo import ModeloCosto, ModeloCostoExtendido

# PESTAÑA 1 -----------------------------------------------------------------------------------------------------
def mostrar_pagina_1(funcion_consumo: ModeloCosto):
    """Contenido de la Página 1."""
    st.markdown('<div class="section-eyebrow">Testeo de la función</div>', unsafe_allow_html=True)
    st.subheader("Cálculo de consumo energético")
    
    if not funcion_consumo:
        st.warning("Por favor, ingresa una función de consumo energético en el sidebar para continuar.")
        return
    
    if 'calculado' not in st.session_state:
        st.session_state.calculado = False
    if 'consumo_energia_data' not in st.session_state:
        st.session_state.consumo_energia_data = None

    if st.session_state.calculado:
        st.markdown('<div class="section-eyebrow">Función de Consumo Energético</div>', unsafe_allow_html=True)
        st.latex(funcion_consumo.funcion)
    
    input_x, input_y, input_z = st.columns(3)
    with input_x:
        x_val = st.number_input(
            "Porcentaje de uso CPU (x)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.get("pagina1_x_val", 70.0)),
            step=1.0,
            key="pagina1_x_val",
        )
    with input_y:
        y_val = st.number_input(
            "Cantidad de RAM utilizada (y)",
            min_value=0.0,
            max_value=64.0,
            value=float(st.session_state.get("pagina1_y_val", 32.0)),
            step=1.0,
            key="pagina1_y_val",
        )
    with input_z:
        z_val = st.number_input(
            "Número de procesos activos (z)",
            min_value=0,
            max_value=1000,
            value=int(st.session_state.get("pagina1_z_val", 120)),
            step=1,
            key="pagina1_z_val",
        )

    if st.button("Calcular Consumo Energético"):
        if 'modelo' in st.session_state and st.session_state.modelo is not None:
            modelo = st.session_state.modelo
            
            consumo = modelo.funcion.subs({modelo.symbols[0]: x_val, modelo.symbols[1]: y_val, modelo.symbols[2]: z_val})
            x_vals = np.linspace(0, 100, 50)
            y_vals = np.linspace(0, 64, 50)
            z_vals = np.linspace(0, 1000, 50)
            X, Y, Z = np.meshgrid(x_vals, y_vals, z_vals, indexing='ij')

            
            F = np.array([modelo.funcion_lambda(x, y, z) for x, y, z in zip(X.flatten(), Y.flatten(), Z.flatten())])
            F = F.reshape(X.shape)

            st.session_state.consumo_energia_data = {
                "x_val": x_val,
                "y_val": y_val,
                "z_val": z_val,
                "consumo": consumo,
                "x_vals": x_vals,
                "y_vals": y_vals,
                "z_vals": z_vals,
                "X": X,
                "Y": Y,
                "Z": Z,
                "F": F,
            }
        else:
            st.error("No se ha cargado un modelo válido. Por favor, ingresa una función válida en el sidebar.")

    consumo_energia_data = st.session_state.consumo_energia_data
    if consumo_energia_data:
        st.success(f"El consumo energético calculado es: {consumo_energia_data['consumo']}")

        x_val = consumo_energia_data["x_val"]
        y_val = consumo_energia_data["y_val"]
        z_val = consumo_energia_data["z_val"]
        X = consumo_energia_data["X"]
        Y = consumo_energia_data["Y"]
        Z = consumo_energia_data["Z"]
        F = consumo_energia_data["F"]

        fig = go.Figure(data=go.Volume(
            x=X.flatten().tolist(),
            y=Y.flatten().tolist(),
            z=Z.flatten().tolist(),
            value=F.flatten().tolist(),
            isomin=float(np.min(F)),
            isomax=float(np.max(F)),
            opacity=0.1,  # Ajusta la opacidad para ver el interior
            surface_count=20,  # Número de superficies de nivel
        )) 

        fig.add_trace(go.Scatter3d(
            x=[x_val],
            y=[y_val],
            z=[z_val],
            mode='markers',
            marker=dict(size=5, color='red'),
            name='Punto de Evaluación'
        ))

        fig.update_layout(scene=dict(
            xaxis_title='CPU (%)',
            yaxis_title='RAM (GB)',
            zaxis_title='Procesos Activos'
        ))
        st.plotly_chart(fig, use_container_width=True)




# PESTAÑA 2 -----------------------------------------------------------------------------------------------------
def mostrar_pagina_2(funcion_consumo: ModeloCosto):
    """Contenido de la Página 2."""
    st.markdown('<div class="section-eyebrow">Análisis de Consumos</div>', unsafe_allow_html=True)
    st.subheader("Superficies y curvas de Nivel")
    
    if not funcion_consumo:
        st.warning("Por favor, ingresa una función de consumo energético en el sidebar para continuar.")
        return
    
    if 'calculado' not in st.session_state:
        st.session_state.calculado = False
    if 'superficie_calculada' not in st.session_state:
        st.session_state.superficie_calculada = False
    if 'superficie_nivel_data' not in st.session_state:
        st.session_state.superficie_nivel_data = None
    
    if st.session_state.calculado:
        st.markdown('<div class="section-eyebrow">Función de Consumo Energético</div>', unsafe_allow_html=True)
        st.latex(funcion_consumo.funcion)
    
    with st.form("form_superficie_nivel", clear_on_submit=False):
        valor_corte = st.slider(
            "Valor de corte para curvas de nivel",
            min_value=0.0,
            max_value=1000.0,
            value=100.0,
            step=10.0,
            key="valor_corte_superficie",
        )
        calcular_superficie = st.form_submit_button("Calcular Superficie de Nivel")

    if calcular_superficie:
        if 'modelo' in st.session_state and st.session_state.modelo is not None:
            modelo = st.session_state.modelo
            soluciones = modelo.calcular_curva_nivel(valor_corte)

            ecuacion_raw = soluciones[0] if soluciones else None
            if ecuacion_raw:
                ecuacion_limpia = ecuacion_raw.simplify()
                x_vals = np.linspace(0, 100, 50)
                y_vals = np.linspace(0, 64, 50)
                X, Y = np.meshgrid(x_vals, y_vals)
                funcion_z = sp.lambdify((modelo.symbols[0], modelo.symbols[1]), ecuacion_limpia, 'numpy')
                Z = funcion_z(X, Y)

                st.session_state.superficie_calculada = valor_corte
                st.session_state.superficie_nivel_data = {
                    "valor_corte": valor_corte,
                    "ecuacion_limpia": ecuacion_limpia,
                    "x_vals": x_vals,
                    "y_vals": y_vals,
                    "X": X,
                    "Y": Y,
                    "Z": Z,
                }
            else:
                st.session_state.superficie_nivel_data = None
                st.warning("No se pudo calcular la curva de nivel para el valor especificado.")
        else:
            st.error("No se ha cargado un modelo válido. Por favor, ingresa una función válida en el sidebar.")

    superficie_nivel_data = st.session_state.superficie_nivel_data
    if superficie_nivel_data:
        ecuacion_limpia = superficie_nivel_data["ecuacion_limpia"]
        valor_corte = superficie_nivel_data["valor_corte"]
        x_vals = superficie_nivel_data["x_vals"]
        y_vals = superficie_nivel_data["y_vals"]
        X = superficie_nivel_data["X"]
        Y = superficie_nivel_data["Y"]
        Z = superficie_nivel_data["Z"]

        st.markdown('<div class="section-eyebrow">Ecuación de Superficie de Nivel</div>', unsafe_allow_html=True)
        st.write(f"La ecuación de la superficie de nivel para E(x,y,z) = {valor_corte} es:")
        st.latex(ecuacion_limpia)

        fig = go.Figure()
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, showscale=False, name='Curva de Nivel'))
        fig.update_layout(scene=dict(
            xaxis_title='CPU (%)',
            yaxis_title='RAM (GB)',
            zaxis_title='Procesos Activos',
        ))
        st.plotly_chart(fig, use_container_width=True)

        with st.form("form_curva_nivel_2d", clear_on_submit=False):
            corte_z = st.slider(
                "Corte en Z para visualizar la curva de nivel",
                min_value=float(np.min(Z)),
                max_value=float(np.max(Z)),
                value=float(np.mean(Z)),
                step=10.0,
                key="corte_z_curva_nivel",
            )
            mostrar_curva_2d = st.form_submit_button("Mostrar Curva de Nivel en 2D")

        if mostrar_curva_2d:
            fig2d = go.Figure()
            fig2d.add_trace(go.Contour(
                z=Z,
                x=x_vals,
                y=y_vals,
                contours=dict(
                    start=corte_z,
                    end=corte_z,
                    size=1,
                    coloring='lines'
                ),
                line=dict(color='red', width=2),
                showscale=False,
                name='Curva de Nivel'
            ))
            fig2d.update_layout(
                xaxis_title='CPU (%)',
                yaxis_title='RAM (GB)',
                title=f'Curva de Nivel para E(x,y,z) = {valor_corte} a Z = {corte_z}'
            )
            st.plotly_chart(fig2d, use_container_width=True)
    





# PESTAÑA 3 -----------------------------------------------------------------------------------------------------
def mostrar_pagina_3(funcion_consumo: ModeloCosto):
    """Contenido de la Página 3."""
    st.markdown('<div class="section-eyebrow">Tasas de cambio</div>', unsafe_allow_html=True)
    st.subheader("Gradiente y derivadas parciales")
    
    if not funcion_consumo:
        st.warning("Por favor, ingresa una función de consumo energético en el sidebar para continuar.")
        return
    
    if 'calculado' not in st.session_state:
        st.session_state.calculado = False

    gradiente = funcion_consumo.gradient 

    col_x , col_y, col_z = st.columns(3)
    with col_x:
        st.markdown('<div class="section-eyebrow">Derivada Parcial con respecto a x</div>', unsafe_allow_html=True)
        st.latex(gradiente[0])
    with col_y:
        st.markdown('<div class="section-eyebrow">Derivada Parcial con respecto a y</div>', unsafe_allow_html=True)
        st.latex(gradiente[1])
    with col_z:
        st.markdown('<div class="section-eyebrow">Derivada Parcial con respecto a z</div>', unsafe_allow_html=True)
        st.latex(gradiente[2])
    
    st.markdown('<div class="section-eyebrow">Evaluación del Gradiente en un Punto</div>', unsafe_allow_html=True)
    input_x, input_y, input_z = st.columns(3)
    with input_x:
        x_val = st.number_input(
            "Porcentaje de uso CPU (x)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.get("pagina3_x_val", 70.0)),
            step=1.0,
            key="pagina3_x_val",
        )
    with input_y:
        y_val = st.number_input(
            "Cantidad de RAM utilizada (y)",
            min_value=0.0,
            max_value=64.0,
            value=float(st.session_state.get("pagina3_y_val", 32.0)),
            step=1.0,
            key="pagina3_y_val",
        )
    with input_z:
        z_val = st.number_input(
            "Número de procesos activos (z)",
            min_value=0,
            max_value=1000,
            value=int(st.session_state.get("pagina3_z_val", 120)),
            step=1,
            key="pagina3_z_val",
        )
    
    if st.button("Evaluar Gradiente"):
        grad_evaluado = funcion_consumo.evaluar_gradiente(x_val, y_val, z_val)
        st.success(f"El gradiente evaluado en el punto ({x_val}, {y_val}, {z_val}) es:")
        st.latex(f"\\nabla E({x_val}, {y_val}, {z_val}) = ({grad_evaluado[0]}, {grad_evaluado[1]}, {grad_evaluado[2]})")
        if grad_evaluado[0] == 0 and grad_evaluado[1] == 0 and grad_evaluado[2] == 0:
            st.info("El gradiente es cero en este punto, lo que indica un posible punto crítico.")
        for i, var in enumerate(funcion_consumo.symbols):
            if grad_evaluado[i] > 0:
                st.info(f"La función aumenta en la dirección positiva de {var}.")
            elif grad_evaluado[i] < 0:
                st.info(f"La función disminuye en la dirección positiva de {var}.")
            else:
                st.info(f"No hay cambio en la dirección de {var}.")




# PESTAÑA 4 -----------------------------------------------------------------------------------------------------
def mostrar_pagina_4(funcion_consumo: ModeloCosto):
    """Contenido de la Página 4."""
    st.markdown('<div class="section-eyebrow">Analisis con gradiente</div>', unsafe_allow_html=True)
    st.subheader("Puntos Críticos")

    if 'modelo' not in st.session_state or st.session_state.modelo is None:
        st.warning("Por favor, ingresa una función de consumo energético en el sidebar para continuar.")
        return
    
    if 'calculado' not in st.session_state:
        st.session_state.calculado = False

    gradiente = funcion_consumo.gradient

    st.markdown('<div class="section-eyebrow">Gradiente de la función</div>', unsafe_allow_html=True)
    st.latex(f"\\nabla E(x, y, z) = ({gradiente[0]}, {gradiente[1]}, {gradiente[2]})")

    if st.button("Calcular Puntos Críticos"):
        puntos_criticos = funcion_consumo.puntos_criticos()
        if puntos_criticos:
            x, y, z = sp.symbols('x y z')
            st.success("Se han encontrado los siguientes puntos críticos:")
            #print(puntos_criticos)
            #print(type(puntos_criticos))
            if isinstance(puntos_criticos, list):
                for i, punto in enumerate(puntos_criticos):
                    st.latex(f"Punto Crítico {i+1}: ({punto[x]}, {punto[y]}, {punto[z]})")
                    if punto[x] > 100 or punto[y] > 64 or punto[z] > 1000:
                        st.warning(f"El punto crítico {i+1} está fuera del rango de los parámetros definidos.")
                    if punto[x] < 0 or punto[y] < 0 or punto[z] < 0:
                        st.error(f"El punto crítico {i+1} tiene valores negativos, lo cual puede no ser válido para los parámetros definidos.")
            else:
                st.latex(f"Punto Crítico: ({puntos_criticos[x]}, {puntos_criticos[y]}, {puntos_criticos[z]})")
                if puntos_criticos[x] > 100 or puntos_criticos[y] > 64 or puntos_criticos[z] > 1000:
                    st.warning("El punto crítico encontrado está fuera del rango de los parámetros definidos.")
                if puntos_criticos[x] < 0 or puntos_criticos[y] < 0 or puntos_criticos[z] < 0:
                    st.error("El punto crítico encontrado tiene valores negativos, lo cual puede no ser válido para los parámetros definidos.")
                
        else:
            st.info("No se encontraron puntos críticos para la función dada.")





def mostrar_pagina_5(funcion_consumo: ModeloCosto):
    """Contenido de la Página 5."""
    st.markdown('<div class="section-eyebrow">Modelo extendido</div>', unsafe_allow_html=True)
    st.subheader("Análisis Avanzado del Consumo Energético")
    
    if not funcion_consumo:
        st.warning("Por favor, ingresa una función de consumo energético en el sidebar para continuar.")
        return
    
    if 'calculado' not in st.session_state:
        st.session_state.calculado = False

    st.markdown('<div class="section-eyebrow">Función de Consumo Energético Extendida</div>', unsafe_allow_html=True)
    st.write("Se ha extendido la función de consumo energético para incluir un parámetro adicional $q$, que representa la frecuencia del procesador. La nueva función es:")
    st.latex("E_{ext}(x, y, z, q) = E(x, y, z) + 18(q - 1.8)^2 + 0.08x(q - 1.8)")

    st.subheader("Comparación entre el modelo original y el extendido")

    x_col, y_col, z_col, q_col = st.columns(4)
    with x_col:
        x_val = st.number_input(
            "Porcentaje de uso CPU (x)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.get("pagina5_x_val", 70.0)),
            step=1.0,
            key="pagina5_x_val",
        )
    with y_col:
        y_val = st.number_input(
            "Cantidad de RAM utilizada (y)",
            min_value=0.0,
            max_value=64.0,
            value=float(st.session_state.get("pagina5_y_val", 32.0)),
            step=1.0,
            key="pagina5_y_val",
        )
    with z_col:
        z_val = st.number_input(
            "Número de procesos activos (z)",
            min_value=0,
            max_value=1000,
            value=int(st.session_state.get("pagina5_z_val", 120)),
            step=1,
            key="pagina5_z_val",
        )
    with q_col:
        q_val = st.number_input(
            "Frecuencia procesador (GHz) (q)",
            min_value=0.0,
            max_value=5.0,
            value=float(st.session_state.get("pagina5_q_val", 2.5)),
            step=0.1,
            key="pagina5_q_val",
        )
    
    if st.button("Calcular Consumo Energético Extendida"):
        if 'modelo' in st.session_state and st.session_state.modelo is not None:
            modelo = st.session_state.modelo
            
            consumo_original = modelo.funcion.subs({modelo.symbols[0]: x_val, modelo.symbols[1]: y_val, modelo.symbols[2]: z_val})
            
            modelo_extendido = ModeloCostoExtendido(f"{modelo.funcion} + 18*(q - 1.8)**2 + 0.08*x*(q - 1.8)")
            consumo_extendido = modelo_extendido.funcion.subs({modelo_extendido.symbols[0]: x_val, 
                modelo_extendido.symbols[1]: y_val, 
                modelo_extendido.symbols[2]: z_val,
                modelo_extendido.symbols[3]: q_val})
            st.session_state.consumo_energia_extendido = {
                "x_val": x_val,
                "y_val": y_val,
                "z_val": z_val,
                "q_val": q_val,
                "consumo_original": consumo_original,
                "consumo_extendido": consumo_extendido,
            }

            st.success(f"El consumo energético original es: {consumo_original}")
            st.success(f"El consumo energético extendido es: {consumo_extendido}")
        else:
            st.error("No se ha cargado un modelo válido. Por favor, ingresa una función válida en el sidebar.")
        
        if 'consumo_energia_extendido' in st.session_state:
            consumo_data = st.session_state.consumo_energia_extendido
            consumo_original = consumo_data["consumo_original"]
            consumo_extendido = consumo_data["consumo_extendido"]

            fig = go.Figure(data=[
                go.Bar(name='Consumo Original', x=['Consumo Energético'], y=[float(consumo_original)], marker_color='indigo'),
                go.Bar(name='Consumo Extendido', x=['Consumo Energético'], y=[float(consumo_extendido)], marker_color='orange')
            ])
            fig.update_layout(barmode='group', title_text='Comparación de Consumo Energético', yaxis_title='Consumo Energético')
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Gradiente de la función original y extendida")
            grad1_col, grad2_col = st.columns(2)
            with grad1_col:
                st.markdown('<div class="section-eyebrow">Gradiente del Modelo Original</div>', unsafe_allow_html=True)
                grad_original = modelo.evaluar_gradiente(x_val, y_val, z_val)
                st.latex(fr'''
                         \nabla E(x, y, z) =
                         \begin{{bmatrix}}
                         \ {grad_original[0]} \\
                         \ {grad_original[1]} \\
                         \ {grad_original[2]}
                         \end{{bmatrix}}
                         ''')
            with grad2_col:
                st.markdown('<div class="section-eyebrow">Gradiente del Modelo Extendido</div>', unsafe_allow_html=True)
                grad_extendido = modelo_extendido.evaluar_gradiente(x_val, y_val, z_val, q_val)
                st.latex(fr'''
                         \nabla E_{{ext}}(x, y, z, q) =
                         \begin{{bmatrix}}
                         \ {grad_extendido[0]} \\
                         \ {grad_extendido[1]} \\
                         \ {grad_extendido[2]} \\
                         \ {grad_extendido[3]}
                         \end{{bmatrix}}
                         ''')