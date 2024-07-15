import streamlit as st
from user_management import UserManagement
import datetime

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

# Función para la consulta de documentos
def consulta_documentos():
    st.title("Consultar Estado del Caso")
    with st.form("check_status_form"):
        case_code = st.text_input("Código del Caso")
        check_button = st.form_submit_button("Consultar Estado")
        if check_button:
            case = user_management.get_case_by_code(case_code)
            if case:
                st.session_state.case_info = case
                st.session_state.show_case_info = True
                st.experimental_rerun()
            else:
                st.warning("El caso no existe")

# Función para mostrar la información del documento
def mostrar_informacion_del_documento(case):
    st.title("Información del Caso")

    # Mostrar la etapa del caso con los colores adecuados
    stages = ["preparatoria", "intermedia", "juzgamiento"]
    current_stage_index = stages.index(case['stage'])

    st.write("**Progreso del Caso:**")
    cols = st.columns(len(stages) * 2 - 1)  # Create extra columns for the lines between circles
    for i, stage in enumerate(stages):
        if i < current_stage_index:
            circle_color = "background-color: black; color: white;"
        elif i == current_stage_index:
            circle_color = "background-color: blue; color: white;"
        else:
            circle_color = "background-color: white; color: black;"

        cols[i * 2].markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="{circle_color} border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; font-weight: bold;">
                    {i + 1}
                </div>
                <div style="margin-top: 5px;">
                    {stage.capitalize()}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if i < len(stages) - 1:
            cols[i * 2 + 1].markdown(f"""
                <div style="background-color: lightgray; height: 2px; width: 100%; margin-top: 22px;"></div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Mostrar la información del caso
    st.write(f"**Código del Caso:** {case['code']}")
    st.write(f"**Apellidos del Investigado:** {case['investigated_last_name']}")
    st.write(f"**Nombre del Investigado:** {case['investigated_first_name']}")
    st.write(f"**DNI del Investigado:** {case['dni']}")
    st.write(f"**Encargado de Revisar el Caso:** {case['reviewer']}")
    st.write(f"**Fecha de Creación:** {case['created_date']}")

    # Calcular la fecha de entrega
    if isinstance(case['created_date'], str):
        created_date = datetime.datetime.strptime(case['created_date'], "%Y-%m-%d").date()
    else:
        created_date = case['created_date']
    
    if isinstance(case['deadline'], str):
        delivery_date = datetime.datetime.strptime(case['deadline'], "%Y-%m-%d").date()
    else:
        delivery_date = case['deadline']
    
    st.write(f"**Fecha de Entrega:** {delivery_date.strftime('%Y-%m-%d')}")

    st.write(f"**Etapa del Caso:** {case['stage']}")

    st.markdown("---")
    if st.button("Regresar a Inicio"):
        st.session_state.show_case_info = False
        st.experimental_rerun()
