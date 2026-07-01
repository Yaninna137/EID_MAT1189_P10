import streamlit as st
from component.css import css

# 1. Configuración global (debe ir al principio del script)
st.set_page_config(
    page_title="Mi Panel de Control",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectamos el CSS personalizado
st.markdown(css(), unsafe_allow_html=True)

# 2. Definición de los pasos del recorrido (puedes cambiar los nombres aquí)
PASOS_RECORRIDO = [
    "Configuración",
    "Análisis de Datos",
    "Métricas Clave",
    "Visualización Final"
]

# 3. Inicializar el estado de la sesión para controlar la navegación
if "paso_actual" not in st.session_state:
    st.session_state.paso_actual = 0

# ---------------------------------------------------------------------------
# MENÚ LATERAL (st.sidebar): Entrada de datos y opciones persistentes
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Panel de Exposición")
    
    # Selector directo para saltar a cualquier paso (se sincroniza bidireccionalmente)
    paso_seleccionado = st.radio(
        "Recorrido del flujo",
        options=list(range(len(PASOS_RECORRIDO))),
        format_func=lambda idx: f"{idx + 1}. {PASOS_RECORRIDO[idx]}",
        index=st.session_state.paso_actual,
    )
    if paso_seleccionado != st.session_state.paso_actual:
        st.session_state.paso_actual = paso_seleccionado
        st.rerun()
        
    st.divider()
    st.subheader("Añadir Datos Extra")
    dato_usuario = st.text_input("Ingresa un dato:", placeholder="Ejemplo: Valor X")
    if st.button("Procesar Entrada", use_container_width=True):
        st.success(f"Dato '{dato_usuario}' recibido")

# ---------------------------------------------------------------------------
# ÁREA PRINCIPAL: Renderizado condicional basado en el paso actual
# ---------------------------------------------------------------------------
paso_activo = st.session_state.paso_actual

# Encabezado dinámico fuera del contenedor blanco (mantiene el fondo limpio de la app)
st.markdown(
    f"""
    <div style="margin-bottom: 1.5rem;">
        <span style="color: #c2410c; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">
            Módulo Activo
        </span>
        <h1 style="margin: 0; color: #1f2933;">{PASOS_RECORRIDO[paso_activo]}</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Apertura del contenedor blanco estilizado (únicamente envuelve al contenido de la página)
st.markdown('<div class="blanco-container">', unsafe_allow_html=True)

if paso_activo == 0:
    st.subheader("Paso 1: Inicialización del Entorno")
    st.write("Aquí puedes colocar tus formularios o tablas de carga inicial.")
    st.text_input("Próximos agregados", placeholder="Escribe aquí...", disabled=True)

elif paso_activo == 1:
    st.subheader("Paso 2: Procesamiento y Filtros")
    st.info("Espacio dedicado a mostrar transformaciones de datos o estados lógicos.")

elif paso_activo == 2:
    st.subheader("Paso 3: Visualización de Matrices")
    # Ejemplo de uso de métricas integradas dentro del bloque
    col1, col2 = st.columns(2)
    col1.metric("Variables Detectadas", "42")
    col2.metric("Densidad de Muestreo", "94.5%")

elif paso_activo == 3:
    st.subheader("Paso 4: Reporte de Conclusiones")
    st.success("¡Todo listo! El modelo ha finalizado su ejecución.")

# Cierre del contenedor blanco estilizado
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# CONTROLES INFERIORES: Botones de navegación estilo presentación
# ---------------------------------------------------------------------------
st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
col_anterior, col_estado, col_siguiente = st.columns([1, 2.4, 1])

with col_anterior:
    if st.button("Anterior", use_container_width=True, disabled=paso_activo == 0):
        st.session_state.paso_actual = max(0, paso_activo - 1)
        st.rerun()

with col_estado:
    st.markdown(
        f"""
        <div style="background: #eee6d9; border: 1px solid #d6cbbb; border-radius: 8px; 
                    color: #685f55; min-height: 2.65rem; display: flex; align-items: center; 
                    justify-content: center; font-weight: 750; font-size: 0.9rem;">
            Pantalla {paso_activo + 1} de {len(PASOS_RECORRIDO)} — {PASOS_RECORRIDO[paso_activo]}
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_siguiente:
    if st.button("Siguiente", use_container_width=True, disabled=paso_activo == len(PASOS_RECORRIDO) - 1):
        st.session_state.paso_actual = min(len(PASOS_RECORRIDO) - 1, paso_activo + 1)
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)