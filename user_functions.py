# user_functions.py
import streamlit as st
import pandas as pd
from user_management import UserManagement
from streamlit_option_menu import option_menu

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

# CSS para el tema en azul
st.markdown("""
    <style>
    .main .block-container {
        padding: 1rem 1rem;
    }
    .stSidebar .css-1aumxhk {
        padding: 1rem 1rem;
    }
    .css-1aumxhk h1 {
        color: #1e3a8a; /* Cambia el color a azul */
    }
    .css-vl3ld5 {
        color: #ffffff;
        background-color: #1e3a8a; /* Cambia el color de fondo a azul */
    }
    </style>
    """, unsafe_allow_html=True)

def check_document_status(doc_id):
    return f"Estado del documento {doc_id}: Pendiente"

def login(username, password):
    user = user_management.get_user_by_username(username)
    if user and user['password'] == password:
        st.session_state.authenticated = True
        st.session_state.role = user['role']
        st.session_state.username = username
        st.session_state.user_id = user['user_id']
        st.session_state.password_attempts = 3
        return True
    else:
        st.warning("Nombre de usuario o contraseña inválidos")
        return False

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
                    st.experimental_rerun()
    
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
                st.experimental_rerun()
            
        if main_option == "Ver Documentos":
            st.subheader("Ver Documentos")
            casos = user_management.get_cases_by_reviewer(st.session_state.username)
        
            if casos:
                df = pd.DataFrame(casos)
                df.columns = ['id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'stage']
                df = df.rename(columns={
                    'id': 'ID',
                    'code': 'Código del Documento',
                    'investigated_last_name': 'Apellidos del Investigado',
                    'investigated_first_name': 'Nombre del Investigado',
                    'dni': 'DNI del Investigado',
                    'reviewer': 'Encargado de Revisar el Documento',
                    'stage': 'Etapa',
                })

                for i, row in df.iterrows():
                    cols = st.columns((3, 10, 15, 15, 8, 10, 11))
                    cols[0].write(row['ID'])
                    cols[1].write(row['Código del Documento'])
                    cols[2].write(row['Apellidos del Investigado'])
                    cols[3].write(row['Nombre del Investigado'])
                    cols[4].write(row['DNI del Investigado'])
                    cols[5].write(row['Encargado de Revisar el Documento'])
                    cols[6].write(row['Etapa'])
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
                    update_button = st.form_submit_button("Guardar Cambios")

                    if update_button:
                        user_management.update_user(
                            user_id=user_data['user_id'],
                            username=user_data['username'],
                            password=user_data['password'],
                            role=user_data['role'],
                            first_name=first_name,
                            last_name=last_name,
                            dni=dni
                        )
                        st.success("Datos personales actualizados correctamente")
                        st.experimental_rerun()

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
                                st.success("Se actualizo correctamente su contraseña")
                                #st.experimental_rerun()
                            else:
                                st.warning("Contraseña actual incorrecta")
                        else:
                            st.warning("Las contraseñas nuevas no coinciden")

