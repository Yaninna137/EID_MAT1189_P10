import streamlit as st

def mostrar_sidebar(pasos: list[str]) -> str:
    """Muestra el panel lateral izquierdo de configuración y control."""
    st.sidebar.header("Menú de Configuración")
    
    # Selector en sidebar sincronizado
    paso_elegido = st.sidebar.radio(
        "Ir a sección",
        options=list(range(len(pasos))),
        format_func=lambda idx: f"{idx + 1}. {pasos[idx]}",
        index=st.session_state.paso_actual,
    )
    
    if paso_elegido != st.session_state.paso_actual:
        st.session_state.paso_actual = paso_elegido
        st.rerun()
        
    st.sidebar.divider()
    st.sidebar.subheader("Entrada de Parámetros")
    dato_usuario = st.sidebar.text_input("Ingresa un dato base:", placeholder="Ejemplo: Dataset_01")
    
    if st.sidebar.button("Procesar Configuración", use_container_width=True):
        st.sidebar.success("Parámetro fijado.")
        
    return dato_usuario