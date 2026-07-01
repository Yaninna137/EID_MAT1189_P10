import streamlit as st

def mostrar_menu_horizontal_navegacion(pasos: list[str], paso_actual: int) -> None:
    """Crea una barra horizontal con botones de navegación e interacciones de color."""
    # Columnas proporcionales: Flecha izq, botones dinámicos de páginas, Flecha der
    columnas = st.columns([0.35] + [1.5] * len(pasos) + [0.35])
    
    # 1. Flecha izquierda (‹)
    with columnas[0]:
        if st.button("‹", use_container_width=True, disabled=paso_actual == 0, key="nav_prev_btn"):
            st.session_state.paso_actual = max(0, paso_actual - 1)
            st.rerun()
            
    # 2. Renderizado del menú interactivo por páginas
    for idx, paso in enumerate(pasos):
        with columnas[idx + 1]:
            es_activo = (idx == paso_actual)
            label_boton = f"{idx + 1} • {paso}"
            
            # El CSS captura este tipo para pintar el fondo activo o inactivo
            tipo_boton = "primary" if es_activo else "secondary"
            
            if st.button(label_boton, use_container_width=True, type=tipo_boton, key=f"menu_item_{idx}"):
                st.session_state.paso_actual = idx
                st.rerun()
                
    # 3. Flecha derecha (›)
    with columnas[-1]:
        if st.button("›", use_container_width=True, disabled=paso_actual == len(pasos) - 1, key="nav_next_btn"):
            st.session_state.paso_actual = min(len(pasos) - 1, paso_actual + 1)
            st.rerun()
            
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)