import streamlit as st
import plotly.graph_objects as go
import numpy as np
from model.modelo import ModeloCosto

def mostrar_pagina_1(funcion_consumo: str):
    """Contenido de la Página 1."""
    st.markdown('<div class="section-eyebrow">Testeo de la función</div>', unsafe_allow_html=True)
    st.subheader("Cálculo de consumo energético")
    
    if not funcion_consumo:
        st.warning("Por favor, ingresa una función de consumo energético en el sidebar para continuar.")
        return
    
    input_x, input_y, input_z = st.columns(3)
    with input_x:
        x_val = st.number_input("Porcentaje de uso CPU (x)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
    with input_y:
        y_val = st.number_input("Cantidad de RAM utilizada (y)", min_value=0.0, max_value=64.0, value=16.0, step=1.0)
    with input_z:
        z_val = st.number_input("Número de procesos activos (z)", min_value=0, max_value=1000, value=10, step=1)

    if st.button("Calcular Consumo Energético"):
        if 'modelo' in st.session_state and st.session_state.modelo is not None:
            modelo = st.session_state.modelo
            
            consumo = modelo.funcion.subs({modelo.symbols[0]: x_val, modelo.symbols[1]: y_val, modelo.symbols[2]: z_val})
            st.success(f"El consumo energético calculado es: {consumo}")

            # graficar
            x_vals = np.linspace(0, 100, 50)
            y_vals = np.linspace(0, 64, 50)
            z_vals = np.linspace(0, 1000, 50)
            X, Y, Z = np.meshgrid(x_vals, y_vals, z_vals, indexing='ij')

            
            F = np.array([modelo.funcion_lambda(x, y, z) for x, y, z in zip(X.flatten(), Y.flatten(), Z.flatten())])
            F = F.reshape(X.shape)

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
        else:
            st.error("No se ha cargado un modelo válido. Por favor, ingresa una función válida en el sidebar.")

def mostrar_pagina_2():
    """Contenido de la Página 2."""
    st.markdown('<div class="section-eyebrow">Análisis Intermedio</div>', unsafe_allow_html=True)
    st.subheader("Procesamiento Estadístico")
    
    with st.container():
        st.info("Aquí puedes desplegar tus dataframes, resúmenes cuantitativos o tablas procesadas.")

def mostrar_pagina_3():
    """Contenido de la Página 3."""
    st.markdown('<div class="section-eyebrow">Métricas de Control</div>', unsafe_allow_html=True)
    st.subheader("Indicadores de Rendimiento")
    
    # Al meter las columnas dentro del "with st.container()", todo hereda la misma estructura
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Muestra Total", "0", delta="Esperando modelo")
        col2.metric("Precisión", "0.0%", delta="N/A")
        col3.metric("Tiempo de Respuesta", "0ms")

def mostrar_pagina_4():
    """Contenido de la Página 4."""
    st.markdown('<div class="section-eyebrow">Conclusión Visual</div>', unsafe_allow_html=True)
    st.subheader("Gráficas y Resultados")
    
    with st.container():
        st.warning("Aquí se incrustarán tus gráficos cuando calcules las variables.")