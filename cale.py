# cale.py
import streamlit as st
from user_management import UserManagement
from user_functions import user_interface, check_document_status, login
from admin_functions import admin_interface

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()
user_management.create_default_superusers()

# Simular el estado de autenticación (puede ser mejorado con una solución más segura)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.password_attempts = 3

# Título de la aplicación
st.title("Sistema de Gestión de Casos")

# Página de inicio de sesión y consulta de documentos
if not st.session_state.authenticated:
    st.subheader("Consultar Estado del Caso")
    with st.form("check_status_form"):
        case_code = st.text_input("Código del Caso")
        check_button = st.form_submit_button("Consultar Estado")
        
        if check_button:
            if case_code:
                status = check_document_status(case_code)
                if status:
                    st.info(status)
                else:
                    st.empty()
            else:
                st.warning("Por favor, ingrese un Código del Caso")

    user_interface()
else:
    if st.session_state.role == 'administrador':
        admin_interface()
    else:
        user_interface()
