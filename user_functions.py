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

def calculate_days_left(created_date, deadline):
    today = datetime.date.today()
    deadline_date = pd.to_datetime(deadline).date()
    created_date = pd.to_datetime(created_date).date()
    total_days = (deadline_date - created_date).days
    days_left = (deadline_date - today).days
    return days_left, total_days

def get_semaforo_color(days_left, total_days):
    percentage_left = (days_left / total_days) * 100
    if percentage_left > 50:
        return "🟢"
    elif percentage_left > 20:
        return "🟡"
    else:
        return "🔴"
    
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
                
                # Calcular días restantes y colores de semáforo
                if 'Fecha de Creación' in df.columns and 'Fecha de Entrega' in df.columns:
                    df['days_left'], df['total_days'] = zip(*df.apply(lambda row: calculate_days_left(row['Fecha de Creación'], row['Fecha de Entrega']), axis=1))
                    df['semaforo'] = df.apply(lambda row: get_semaforo_color(row['days_left'], row['total_days']), axis=1)

                # Calcular el estado del caso
                df['state'] = df['Etapa'].apply(lambda x: 'no revisado' if x == 'Preparatoria' else ('en proceso' if x == 'Intermedia' else 'revisado'))

                # Crear el DataFrame final
                df_final = df[['Código del Documento', 'Etapa', 'days_left', 'semaforo', 'state']]

                st.subheader("Resumen de Casos")
                st.dataframe(df_final)

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
