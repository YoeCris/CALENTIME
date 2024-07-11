# cale.py
import streamlit as st
st.set_page_config(page_title="Calentime", page_icon="date", layout="wide")
from user_management import UserManagement
from user_functions import user_interface, check_document_status, login
from admin_functions import admin_interface
import consulta_documentos

#st.set_page_config(page_title="Calentime", page_icon="date", layout="wide")
st.markdown("##")
st.sidebar.image("imagenes/bios.png", caption="Fiscalia Militar")
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
#st.title("Sistema de Gestión de Casos")

# Página de inicio de sesión y consulta de documentos
if not st.session_state.authenticated:
    if 'show_case_info' in st.session_state and st.session_state.show_case_info:
        consulta_documentos.mostrar_informacion_del_documento(st.session_state.case_info)
    else:
        consulta_documentos.consulta_documentos()
        user_interface()
else:
    if st.session_state.role == 'administrador':
        admin_interface()
    else:
        user_interface()