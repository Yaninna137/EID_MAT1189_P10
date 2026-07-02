def css() -> str:
    return """
    <style>
    :root {
        /* Fondos generales de la app (Estilo claro/cálido) */
        --paper: #f6f1e8;
        --paper-soft: #fbf8f1;
        --surface: #fffaf1;
        --surface-strong: #ffffff;

        /* Textos y bordes */
        --ink: #1f2933;
        --muted: #685f55;
        --line: #ded6c9;
        --line-strong: #cdbfae;

        /* Paleta en escala de morados */
        --purple-active: #6D28D9;
        --purple-hover: #8B5CF6;
        --purple-soft: #f3e8ff;
        --purple-border: #d8b4fe;

        /* Botones secundarios de la barra horizontal */
        --button-normal: #F3F4F6;
        --button-border: #E5E7EB;
        --button-text: #374151;

        --coral: #c2410c;
        
        /* Color personalizado para la barra lateral oscura */
        --sidebar-custom: #0E1117;
    }

    /* ==========================================================
       FONDO GENERAL Y TIPOGRAFÍA
    ========================================================== */
    .stApp {
        background: linear-gradient(180deg, var(--paper) 0%, var(--paper-soft) 58%, #ede7db 100%);
        color: var(--ink);
    }

    .main .block-container {
        max-width: 1240px;
        padding-top: 1.25rem;
        padding-bottom: 2.25rem;
    }

    h1, h2, h3, h4 {
        color: var(--ink);
        letter-spacing: 0;
    }

    /* ==========================================================
       CONTENEDOR PRINCIPAL BLANCO
    ========================================================== */
    .blanco-container {
        background-color: var(--surface-strong);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid var(--line);
        box-shadow: 0 10px 24px rgba(37, 42, 48, 0.06);
        color: var(--ink);
        margin-bottom: 1rem;
    }

    /* ==========================================================
       SIDEBAR (Barra lateral oscura con contraste asegurado)
    ========================================================== */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"],
    .stSidebar,
    [data-testid="stSidebarUserContent"] {
        background-color: var(--sidebar-custom) !important;
        border-right: 1px solid #262730;
    }

    /* Forzar contraste de todo el texto dentro de la barra oscura */
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #f7efe3 !important;
    }

    /* Ajuste visual crucial para que los inputs no queden blancos/invisibles en el sidebar */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stTextArea textarea {
        background: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
    }

    /* ==========================================================
       INPUTS GENERALES (Foco Morado)
    ========================================================== */
    .stTextInput input,
    .stTextArea textarea {
        background: #fffdf8;
        color: var(--ink);
        border: 1px solid var(--line-strong);
        border-radius: 8px;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--purple-active);
        box-shadow: 0 0 0 1px var(--purple-active);
    }

    /* ==========================================================
       BOTONES GENERALES DE STREAMLIT (Estilo Morado unificado)
    ========================================================== */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        background: var(--purple-active);
        color: #fffaf1;
        border: 1px solid var(--purple-active);
        border-radius: 8px;
        font-weight: 750;
        min-height: 2.65rem;
        white-space: normal;
        line-height: 1.2;
        transition: all .25s ease;
    }

    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background: var(--purple-hover) !important;
        color: #fffaf1 !important;
        border-color: var(--purple-hover) !important;
    }

    .stButton > button:disabled {
        background: #d8d0c3 !important;
        color: #786f65 !important;
        border-color: #c9beb0 !important;
    }

    /* ==========================================================
       BARRA HORIZONTAL (Comportamiento de botones del Código 2)
    ========================================================== */
    div[data-testid="stHorizontalBlock"] button {
        min-height: 46px;
        font-size: 15px;
        letter-spacing: .2px;
        transition: all .25s ease;
        border-radius: 8px !important;
    }

    /* Botón Activo de la barra horizontal */
    div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"] {
        background: var(--purple-active) !important;
        color: white !important;
        border: 1px solid var(--purple-active) !important;
        font-weight: 700 !important;
        box-shadow: 0 5px 14px rgba(109, 40, 217, 0.22);
    }

    /* Botón Normal de la barra horizontal */
    div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"] {
        background: var(--button-normal) !important;
        color: var(--button-text) !important;
        border: 1px solid var(--button-border) !important;
        font-weight: 600 !important;
    }

    /* Hover del Botón Normal (Se transforma en morado con elevación) */
    div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"]:hover {
        background: var(--purple-hover) !important;
        color: white !important;
        border-color: var(--purple-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(139, 92, 246, 0.28);
        cursor: pointer;
    }

    /* Flechas de navegación específicas de la barra horizontal */
    div[data-testid="stHorizontalBlock"] #nav_prev_btn,
    div[data-testid="stHorizontalBlock"] #nav_next_btn {
        background: var(--button-normal) !important;
        color: var(--button-text) !important;
        border: 1px solid var(--button-border) !important;
        font-weight: 700;
    }

    div[data-testid="stHorizontalBlock"] #nav_prev_btn:hover,
    div[data-testid="stHorizontalBlock"] #nav_next_btn:hover {
        background: var(--purple-hover) !important;
        color: white !important;
        border-color: var(--purple-hover) !important;
    }

    /* ==========================================================
       TÍTULOS Y RECTÁNGULOS DE SECCIÓN
    ========================================================== */
    .app-main-title-container {
        margin-bottom: 1.2rem;
        padding-left: 0.25rem;
    }
    
    .app-main-title {
        font-size: 2.25rem;
        font-weight: 900;
        color: var(--ink);
        margin: 0;
        line-height: 1.1;
    }

    .section-eyebrow {
        color: var(--coral);
        font-size: 0.78rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 0;
        margin-bottom: 0.3rem;
    }

    /* ==========================================================
       CORRECCIÓN AVANZADA PARA INPUTS NUMÉRICOS EN EL SIDEBAR
    ========================================================== */
    /* Fondo, texto y borde general de la casilla */
    [data-testid="stSidebar"] .stNumberInput input {
        background: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4a5568 !important; /* Borde gris oscuro más amigable */
        border-right: none !important; /* Evita doble borde con los botones */
    }

    /* Contenedor completo de la casilla interna de Streamlit */
    [data-testid="stSidebar"] .stNumberInput div[data-baseweb="input"] {
        background-color: #262730 !important;
        border-radius: 8px !important;
        border: 1px solid #4a5568 !important; /* Color de borde unificado */
    }

    /* Forzar el fondo oscuro en el bloque de los botones (+ / -) para que dejen de ser blancos */
    [data-testid="stSidebar"] .stNumberInput div[data-baseweb="input"] div {
        background-color: #262730 !important;
    }

    /* Estilo e íconos para cada botón (+ y -) individualmente */
    [data-testid="stSidebar"] .stNumberInput button {
        background-color: #262730 !important;
        color: #ffffff !important; /* Hace visibles los signos + y - */
        border: none !important;
        opacity: 0.8;
        transition: all 0.2s ease;
    }

    /* Efecto hover sobre los botones + y - */
    [data-testid="stSidebar"] .stNumberInput button:hover {
        background-color: #363942 !important;
        color: var(--purple-hover) !important; /* Destello morado sutil al pasar el mouse */
        opacity: 1;
    }
    </style>
    """