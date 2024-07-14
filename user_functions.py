import streamlit as st
import pandas as pd
from user_management import UserManagement
from streamlit_option_menu import option_menu
import datetime

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

def check_document_status(case_code):
    case = user_management.get_case_by_code(case_code)
    if case:
        return f"Estado del documento {case_code}: {case['stage']}"
    else:
        st.warning("El caso no existe")

def login(username, password):
    user = user_management.get_user_by_username(username)
    if user and user['password'] == password:
        st.session_state.authenticated = True
        st.session_state.role = user['role']
        st.session_state.username = username
        st.session_state.first_name = user['first_name']
        st.session_state.user_id = user['user_id']
        st.session_state.password_attempts = 3
        return True
    else:
        st.warning("Nombre de usuario o contraseña inválidos")
        return False

def calculate_progress(created_date, deadline):
    total_time = (deadline - created_date).days
    elapsed_time = (datetime.datetime.now() - created_date).days
    progress = min(1, max(0, elapsed_time / total_time))
    return progress

def get_progress_color(progress):
    if progress <= 0.5:
        return "green"
    elif progress <= 0.8:
        return "yellow"
    else:
        return "red"

def render_progress_bar(progress):
    color = get_progress_color(progress)
    percentage = int(progress * 100)
    bar_html = f"""
    <div style="background-color: #e0e0e0; border-radius: 5px; width: 100%; height: 20px;">
        <div style="background-color: {color}; width: {percentage}%; height: 100%; border-radius: 5px;"></div>
    </div>
    """
    return bar_html

def user_interface():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None

    if not st.session_state.authenticated:
        st.sidebar.subheader("Iniciar Sesión")
        
        with st.sidebar.form("login_form"):
            username = st.text_input("Nombre de usuario")
            password = st.text_input("Contraseña", type='password')
            login_button = st.form_submit_button("Iniciar Sesión")
            
            if login_button:
                if login(username, password):
                    st.rerun()
    
    if st.session_state.authenticated:
        with st.sidebar:
            main_option = option_menu(
                "MENÚ",
                ["Ver Documentos", "Administrar Mi Usuario", "Cerrar Sesión"],
                icons=["eye", "person", "box-arrow-in-left"],
                menu_icon="cast",
                default_index=0,
            )
            
            if main_option == "Cerrar Sesión":
                st.session_state.authenticated = False
                st.session_state.role = None
                st.session_state.username = None
                st.rerun()

        if main_option == "Ver Documentos":
            st.subheader("Ver Documentos")
            casos = user_management.get_cases_by_reviewer(st.session_state.first_name)

            if casos:
                df = pd.DataFrame(casos)
                df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'created_date', 'deadline', 'stage']

                # Eliminar la columna 'reviewer' si no se necesita mostrar
                df = df.drop(columns=['reviewer'])

                # Renombrar columnas
                df = df.rename(columns={
                    'case_id': 'ID',
                    'code': 'Código del Documento',
                    'investigated_last_name': 'Apellidos del Investigado',
                    'investigated_first_name': 'Nombre del Investigado',
                    'dni': 'DNI del Investigado',
                    'created_date': 'Fecha de Creación',
                    'deadline': 'Fecha de Entrega',
                    'stage': 'Etapa',
                })

                # Calcular y agregar barra de progreso
                df['Progreso'] = df.apply(lambda row: calculate_progress(row['Fecha de Creación'], row['Fecha de Entrega']), axis=1)
                df['Barra de Progreso'] = df['Progreso'].apply(render_progress_bar)

                # Mostrar el DataFrame con barras de progreso simples
                st.write(df.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.warning("No hay documentos disponibles para mostrar.")

        elif main_option == "Administrar Mi Usuario":
            sub_option = option_menu(
                "Administrar Mi Usuario",
                ["Datos Personales", "Cambiar Contraseña"],
                icons=["person", "key"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
            )

            if sub_option == "Datos Personales":
                user_data = user_management.get_user_by_username(st.session_state.username)
                st.subheader("Datos Personales")
                with st.form("personal_data_form"):
                    first_name = st.text_input("Nombres", value=user_data['first_name'], disabled=True)
                    last_name = st.text_input("Apellidos", value=user_data['last_name'], disabled=True)
                    dni = st.text_input("DNI", value=user_data['dni'], disabled=True)
                    number_phone = st.text_input("Número de Celular", value=user_data['number_phone'], disabled=False)
                    update_button = st.form_submit_button("Guardar Cambios")

                    if update_button:
                        user_management.update_user(
                            user_id=user_data['user_id'],
                            username=user_data['username'],
                            password=user_data['password'],
                            role=user_data['role'],
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            dni=user_data['dni'],
                            number_phone=number_phone
                        )
                        st.success("Datos personales actualizados correctamente")
                        st.rerun()

            elif sub_option == "Cambiar Contraseña":
                st.subheader("Cambiar Contraseña")
                with st.form("change_password_form"):
                    current_password = st.text_input("Contraseña Actual", type='password')
                    new_password = st.text_input("Nueva Contraseña", type='password')
                    confirm_password = st.text_input("Repetir Contraseña", type='password')
                    change_password_button = st.form_submit_button("Guardar Cambios")

                    if change_password_button:
                        if new_password == confirm_password:
                            user = user_management.get_user_by_username(st.session_state.username)
                            if user and user['password'] == current_password:
                                user_management.update_user_password(st.session_state.username, new_password)
                                st.success("Se actualizó correctamente su contraseña")
                                st.rerun()
                            else:
                                st.warning("Contraseña actual incorrecta")
                        else:
                            st.warning("Las contraseñas nuevas no coinciden")