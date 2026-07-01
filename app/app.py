import streamlit as st
from component.css import css

# Importaciones modulares de la interfaz
from ui.sidebar import mostrar_sidebar
from ui.layout import mostrar_menu_horizontal_navegacion
from ui.sections import (
    mostrar_pagina_1,
    mostrar_pagina_2,
    mostrar_pagina_3,
    mostrar_pagina_4
)

def main():
    # 1. Configuración de página e inyección del nuevo CSS Morado
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown(css(), unsafe_allow_html=True)
    
    # 2. Inicialización del estado de sesión para el paso activo
    if "paso_actual" not in st.session_state:
        st.session_state.paso_actual = 0
        
    PASOS_PANEL = ["Consumo Energético", "Curvas de Nivel", "Gradiente y Derivadas", "Plano Tangente", "Puntos Críticos"]
    
    # 3. Renderizar Sidebar lateral (Ahora con el color por defecto de Streamlit)
    dato_base = mostrar_sidebar(PASOS_PANEL)
    
    # 4. NOMBRE DE LA PÁGINA (Aparece arriba del menú de páginas)
    st.markdown(
        """
        <div class="app-main-title-container">
            <span class="section-eyebrow">Proyecto 10</span>
            <h1 class="app-main-title">Modelación del consumo energético de un sistema computacional</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 5. Renderizar el menú de línea horizontal interactivo
    mostrar_menu_horizontal_navegacion(PASOS_PANEL, st.session_state.paso_actual)
    
    # 6. Despacho del enrutador dinámico (Contenido en bloque blanco)
    paso_activo = st.session_state.paso_actual
    
    if paso_activo == 0:
        mostrar_pagina_1(dato_base)
    elif paso_activo == 1:
        mostrar_pagina_2()
    elif paso_activo == 2:
        mostrar_pagina_3()
    elif paso_activo == 3:
        mostrar_pagina_4()
    elif paso_activo == 4:
        st.warning("Sección de Puntos Críticos aún en desarrollo. Pronto estará disponible.")

if __name__ == "__main__":
    main()