import streamlit as st

def mostrar_sidebar():
    """
    Renderiza el sidebar con el modelo simplificado y el formulario de edición de datos.
    Retorna un diccionario con los valores actuales de los coeficientes a, b, c, d, e, f, g.
    """
    # 1. Inicializar coeficientes en el session_state si no existen (Valores por defecto)
    valores_por_defecto = {
        "a": 55.0, "b": 0.65, "c": 1.2, "d": 0.08, "e": 0.01, "f": 0.04, "g": 0.0015
    }
    for clave, valor in valores_por_defecto.items():
        if f"coef_{clave}" not in st.session_state:
            st.session_state[f"coef_{clave}"] = valor

    with st.sidebar:
        st.header("Modelo Simplificado")
        st.write(
            "Representar el aumento del consumo energético a medida que crece la "
            "carga computacional, mediante el sig. modelo:"
        )
        
        # 2. Recuperar valores actuales del estado para construir el LaTeX dinámico
        va = st.session_state["coef_a"]
        vb = st.session_state["coef_b"]
        vc = st.session_state["coef_c"]
        vd = st.session_state["coef_d"]
        ve = st.session_state["coef_e"]
        vf = st.session_state["coef_f"]
        vg = st.session_state["coef_g"]
        
        # Código LaTeX dinámico que muestra los valores numéricos actuales
        st.latex("E(x , y, z) = ")
        st.latex(f"{va} + {vb}x + {vc}y + {vd}z + {ve}xy + {vf}yz + {vg}xz")
        
        # Botón Calcular principal
        btn_calcular = st.button("Calcular", key="btn_calcular_main", use_container_width=True)
        if btn_calcular:
            st.success("¡Cálculo ejecutado con los datos actuales!")
            st.session_state.calculado = True

        st.markdown("---")
        st.subheader("Editar Datos")

        # Definición de la estructura de datos para asegurar el orden y alineación por filas
        campos = [
            {"letra": "A", "var": "a", "desc": "El consumo base del sistema"},
            {"letra": "B", "var": "b", "desc": "La contribución individual de cada recurso"},
            {"letra": "C", "var": "c", "desc": "La contribución individual de cada recurso"},
            {"letra": "D", "var": "d", "desc": "La contribución individual de cada recurso"},
            {"letra": "E", "var": "e", "desc": "Las interacciones entre las variables"},
            {"letra": "F", "var": "f", "desc": "Las interacciones entre las variables"},
            {"letra": "G", "var": "g", "desc": "Las interacciones entre las variables"}
        ]

        valores_recuperados = {}

        # Renderizar cada campo fila por fila garantizando alineación exacta
        for campo in campos:
            col_letra, col_significado, col_input = st.columns([1, 4, 3])
            
            with col_letra:
                st.markdown(f"<div style='padding-top: 5px;'><b>{campo['letra']}:</b></div>", unsafe_allow_html=True)
                
            with col_significado:
                st.markdown(f"<div style='font-size: 11px; color: #ded6c9; padding-top: 5px; line-height: 1.2;'>{campo['desc']}</div>", unsafe_allow_html=True)
                
            with col_input:
                # Al cambiar el número, modifica directamente el session_state e impacta al LaTeX superior
                valores_recuperados[campo['var']] = st.number_input(
                    label=campo['var'], 
                    label_visibility="collapsed", 
                    key=f"coef_{campo['var']}", 
                    step=0.1
                )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón para cargar/actualizar los datos explicitamente en la UI
        btn_cargar = st.button("Cargar datos", key="btn_cargar_datos", use_container_width=True)
        if btn_cargar:
            st.toast("Datos cargados y aplicados correctamente", icon="💾")
            # Forzamos un rerun estructural para refrescar instantáneamente el componente LaTeX
            st.rerun()

    # Retornamos un diccionario con todos los coeficientes actuales
    datos_actuales = {
        "a": valores_recuperados["a"],
        "b": valores_recuperados["b"],
        "c": valores_recuperados["c"],
        "d": valores_recuperados["d"],
        "e": valores_recuperados["e"],
        "f": valores_recuperados["f"],
        "g": valores_recuperados["g"],
        "calcular_clicado": btn_calcular,
        "cargar_clicado": btn_cargar
    }

    funcion = f"{datos_actuales['a']} + {datos_actuales['b']}*x + {datos_actuales['c']}*y + {datos_actuales['d']}*z + {datos_actuales['e']}*x*y + {datos_actuales['f']}*y*z + {datos_actuales['g']}*x*z"
    
    return funcion