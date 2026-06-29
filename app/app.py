import streamlit as st
from core.state import inicializar_session_state
from component.css import css

# Configuración de la página para usar el ancho completo
st.set_page_config(layout="wide")
st.markdown(css(), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DISEÑO DE LA PÁGINA: Dividido en 2 columnas (Izquierda estrecha, Derecha amplia)
# ---------------------------------------------------------------------------
col_izquierda, col_derecha = st.columns([1, 3])

# --- LADO IZQUIERDO: Menú lateral de entrada de datos (Ancho menor a la mitad) ---
with col_izquierda:
    st.subheader("Menú de Configuración")
    
    # Input de texto y botón
    dato_usuario = st.text_input("Ingresa un dato:")
    boton_enviar = st.button("Enviar")


# --- LADO DERECHO: Título, pestañas y contenedor con fondo blanco ---
with col_derecha:
    # Título principal
    st.title("Panel de Visualización")
    
    # Barra de recorrido / Pestañas (4 pestañas)
    tab1, tab2, tab3, tab4 = st.tabs(["Página 1", "Página 2", "Página 3", "Página 4"])
    
    # Contenido de las pestañas (dentro del contenedor blanco)
    with tab1:
        st.markdown('<div class="blanco-container">', unsafe_allow_html=True)
        
        # Campo de texto falso (Placeholder)
        st.text_input("Próximos agregados", value="", placeholder="Escribe aquí...", disabled=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="blanco-container">', unsafe_allow_html=True)
        st.info("Contenido de la Página 2")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="blanco-container">', unsafe_allow_html=True)
        st.info("Contenido de la Página 3")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab4:
        st.markdown('<div class="blanco-container">', unsafe_allow_html=True)
        st.info("Contenido de la Página 4")
        st.markdown('</div>', unsafe_allow_html=True)