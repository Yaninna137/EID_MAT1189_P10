def css():
    return """
    <style>
    /* Fondo degradado suave para toda la aplicación */
    .stApp {
        background: linear-gradient(180deg, #f6f1e8 0%, #fbf8f1 58%, #ede7db 100%) !important;
        color: #1f2933;
    }

    /* Contenedor blanco para las secciones activas */
    .blanco-container {
        background-color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 8px;
        border: 1px solid #ded6c9;
        box-shadow: 0 10px 24px rgba(37, 42, 48, 0.06);
        color: #1f2933;
        margin-bottom: 1rem;
    }

    /* Estilización de los inputs de texto dentro del área principal */
    .stTextInput input, .stTextArea textarea {
        background: #fffdf8 !important;
        border: 1px solid #cdbfae !important;
        border-radius: 8px !important;
        color: #1f2933 !important;
    }
    
    /* Modificación de los botones primarios para usar tonos verde/turquesa */
    .stButton > button {
        background: #0f766e !important;
        color: #fffaf1 !important;
        border: 1px solid #0b5f58 !important;
        border-radius: 8px !important;
        font-weight: 750 !important;
    }
    
    .stButton > button:hover {
        background: #0b5f58 !important;
        border-color: #083f3b !important;
    }
    </style>
    """