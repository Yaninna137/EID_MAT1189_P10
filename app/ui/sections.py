import streamlit as st

def mostrar_pagina_1(dato_base: str):
    """Contenido de la Página 1."""
    st.markdown('<div class="section-eyebrow">Paso Inicial</div>', unsafe_allow_html=True)
    st.subheader("Configuración y Carga de Datos")
    
    # Usamos un contenedor nativo de Streamlit
    with st.container():
        st.write(f"**Parámetro activo desde el Sidebar:** `{dato_base if dato_base else 'Ninguno'}`")
        st.text_input("Próximos agregados", value="", placeholder="Escribe aquí cuando tu modelo esté listo...", disabled=True)

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