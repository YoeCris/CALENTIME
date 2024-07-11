import streamlit as st
import pandas as pd
from user_management import UserManagement
from streamlit_option_menu import option_menu
import datetime
import matplotlib.pyplot as plt
import plotly.express as px

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

def show_progress_bar(case):
    created_date = pd.to_datetime(case['created_date'])
    deadline = pd.to_datetime(case['deadline'])
    status = case.get('stage', 'No Revisado')
    current_date = pd.to_datetime('today')
    days_elapsed = (current_date - created_date).days
    total_days = (deadline - created_date).days
    progress = min(100, max(0, (days_elapsed / total_days) * 100))

    bar_color = 'red'
    if progress <= 50:
        bar_color = 'green'
    elif 50 < progress <= 75:
        bar_color = 'orange'

    st.progress(progress / 100, f"{status} ({days_elapsed} días / {total_days} días)", color=bar_color)

    if status == "No Revisado":
        if st.button(f"Iniciar Revisión - {case['code']}", key=f"start_{case['case_id']}"):
            user_management.update_case_status(case['case_id'], "En Revisión")
            st.experimental_rerun()
    elif status == "En Revisión":
        if st.button(f"Entregar Caso - {case['code']}", key=f"finish_{case['case_id']}"):
            user_management.update_case_status(case['case_id'], "Revisado")
            st.experimental_rerun()

def admin_interface():
    with st.sidebar:
        main_option = option_menu(
            "MENÚ",
            ["Visualización", "Administrar Casos", "Administrar Usuarios", "Cerrar Sesión"],
            icons=["eye", "folder", "person", "box-arrow-in-left"],
            menu_icon="cast",
            default_index=0,
        )
        
        if main_option == "Cerrar Sesión":
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.username = None
            st.experimental_rerun()

    if main_option == "Visualización":
        st.subheader("Visualización de Métricas y Progresos")
        
        # Obtener todos los casos
        casos = user_management.get_all_cases()
        
        if casos:
            df = pd.DataFrame(casos)
            df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'created_date', 'deadline', 'stage']

            col1, col2 = st.columns(2)

            with col1:
                # Gráfico de distribución de casos por etapa
                fig1 = px.histogram(df, x='stage', title='Distribución de Casos por Etapa')
                st.plotly_chart(fig1)

                # Gráfico de progreso por encargado
                reviewers = df['reviewer'].unique()
                progress_data = []
                for reviewer in reviewers:
                    reviewer_cases = df[df['reviewer'] == reviewer]
                    total_cases = len(reviewer_cases)
                    reviewed_cases = len(reviewer_cases[reviewer_cases['stage'] == 'Revisado'])
                    progress = (reviewed_cases / total_cases) * 100 if total_cases > 0 else 0
                    progress_data.append({'reviewer': reviewer, 'progress': progress})
                progress_df = pd.DataFrame(progress_data)

                fig3 = px.bar(progress_df, x='reviewer', y='progress', title='Progreso de Revisión por Encargado')
                st.plotly_chart(fig3)

            with col2:
                # Gráfico de distribución de casos por encargado y etapas
                fig2 = px.bar(
                    df, 
                    x='reviewer', 
                    color='stage', 
                    barmode='group', 
                    title='Distribución de Casos por Encargado y Etapa'
                )
                st.plotly_chart(fig2)

                # Gráfico de casos por estado
                status_counts = df['stage'].value_counts().reset_index()
                status_counts.columns = ['stage', 'count']
                fig4 = px.pie(status_counts, values='count', names='stage', title='Estado de los Casos')
                st.plotly_chart(fig4)

            # Tabla de resumen de casos por encargado
            st.subheader("Resumen de Casos por Encargado")
            reviewer_summary = df.groupby('reviewer').agg({
                'code': 'count',
                'stage': lambda x: (x == 'Revisado').sum()
            }).reset_index()
            reviewer_summary.columns = ['Encargado', 'Total de Casos', 'Casos Revisados']
            reviewer_summary['Casos Pendientes'] = reviewer_summary['Total de Casos'] - reviewer_summary['Casos Revisados']
            st.dataframe(reviewer_summary)
        
        else:
            st.warning("No hay casos disponibles para mostrar.")
            
    elif main_option == "Administrar Casos":
        sub_option = option_menu(
                "Administrar Casos",
                ["Agregar Caso", "Modificar Caso"],
                icons=["folder-plus", "pencil"],
                menu_icon="folder",
                default_index=0,
                orientation="horizontal",
            )
        if sub_option == "Agregar Caso":
            st.subheader("Agregar Nuevo Caso")
            with st.form("add_case_form"):
                code = st.text_input("Código del Caso")
                investigated_last_name = st.text_input("Apellidos del Investigado")
                investigated_first_name = st.text_input("Nombre del Investigado")
                dni = st.text_input("DNI del Investigado", max_chars=8)
                created_date = st.date_input("Fecha de Creación", value=datetime.date.today())
                deadline = st.date_input("Fecha de Entrega", value=datetime.date.today())

                if len(dni) != 8 or not dni.isdigit():
                    dni = ""

                users = user_management.get_users()
                normal_users = [user['first_name'] for user in users if user['role'] == 'usuario']
                reviewer = st.selectbox("Encargado de Revisar el Caso", normal_users)

                stage = st.selectbox("Etapa del caso", ['Preparatoria', 'Intermedia', 'Juzgamiento'])

                add_case_button = st.form_submit_button("Agregar Caso")
        
                if add_case_button:
                    if dni:
                        user_management.create_case(code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage)
                        st.success(f"Caso {code} agregado exitosamente")
                        #st.experimental_rerun()

        elif sub_option == "Modificar Caso":
            st.subheader("Editar o Eliminar Caso")

            casos = user_management.get_all_cases()
            if casos:
                df = pd.DataFrame(casos)
                df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'created_date', 'deadline',  'stage']
                df = df.rename(columns={
                    'case_id': 'ID',
                    'code': 'Código',
                    'investigated_last_name': 'Apellidos',
                    'investigated_first_name': 'Nombres',
                    'dni': 'DNI',
                    'reviewer': 'Encargado',
                    'created_date': 'Fecha de Creación',
                    'deadline': 'Fecha de Entrega',
                    'stage': 'Etapa',
                })

                for i, row in df.iterrows():
                    cols = st.columns((3, 10, 15, 15, 8, 15, 13, 10, 10, 4, 4))
                    cols[0].write(row['ID'])
                    cols[1].write(row['Código'])
                    cols[2].write(row['Apellidos'])
                    cols[3].write(row['Nombres'])
                    cols[4].write(row['DNI'])
                    cols[5].write(row['Encargado'])
                    cols[6].write(row['Etapa'])
                    cols[7].write(row['Fecha de Creación'])
                    cols[8].write(row['Fecha de Entrega'])
                    edit_button = cols[9].button("✏️", key=f"edit_{row['ID']}")
                    delete_button = cols[10].button("🗑️", key=f"delete_{row['ID']}")
                    
                    if edit_button:
                        st.session_state.edit_case = user_management.get_case(row['ID'])
                        st.experimental_rerun()
                    
                    if delete_button:
                        user_management.delete_case(row['ID'])
                        st.success(f"Caso con ID {row['ID']} eliminado exitosamente")
                        #st.experimental_rerun()

            else:
                st.warning("No hay casos disponibles para mostrar.")

            if 'edit_case' in st.session_state:
                case = st.session_state.edit_case
                with st.form("edit_case_form"):
                    code = st.text_input("Código del Caso", value=case.get('code', ''))
                    investigated_last_name = st.text_input("Apellidos del Investigado", value=case.get('investigated_last_name', ''))
                    investigated_first_name = st.text_input("Nombre del Investigado", value=case.get('investigated_first_name', ''))
                    dni = st.text_input("DNI del Investigado", value=case.get('dni', ''), max_chars=8)
                    created_date = st.date_input("Fecha de Creación", value=pd.to_datetime(case.get('created_date')))
                    deadline = st.date_input("Fecha de entrega", value=pd.to_datetime(case.get('deadline')))
            
                    if len(dni) != 8 or not dni.isdigit():
                        st.warning("DNI inválido")
                        dni = ""
            
                    users = user_management.get_users()
                    normal_users = [user['first_name'] for user in users if user['role'] == 'usuario']
                    reviewer = st.selectbox("Encargado de Revisar el Caso", normal_users, index=normal_users.index(case.get('reviewer', '')))

                    stage = st.selectbox("Etapa del Caso", ['Preparatoria', 'Intermedia', 'Juzgamiento'], index=['preparatoria', 'intermedia', 'juzgamiento'].index(case.get('stage', 'preparatoria')))
                    edit_case_button = st.form_submit_button("Actualizar Caso")

                    if edit_case_button and dni:
                        user_management.update_case(case['case_id'], code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage)
                        st.success(f"Caso {code} actualizado exitosamente")
                        st.session_state.pop('edit_case')
                        #st.experimental_rerun()

    elif main_option == "Administrar Usuarios":
        st.subheader("Administrar Usuarios")

        sub_option = option_menu(
                "Administar Usuarios",
                ["Agregar Usuario", "Modificar Usuario"],
                icons=["person-plus", "pencil"],
                menu_icon="person",
                default_index=0,
                orientation="horizontal",
            )
        if sub_option == "Agregar Usuario":
            st.subheader("Agregar Nuevo Usuario")
            with st.form("add_user_form"):
                first_name = st.text_input("Nombres")
                last_name = st.text_input("Apellidos")
                dni = st.text_input("DNI", max_chars=8)
                number_phone = st.text_input("Celular", max_chars=9)
                username = st.text_input("Nombre de Usuario")
                password = st.text_input("Contraseña", type='password')
                role = st.selectbox("Rol", ["administrador", "usuario"])
                add_user_button = st.form_submit_button("Agregar Usuario")

                if add_user_button:
                    if len(dni) == 8 and dni.isdigit():
                        user_management.create_user(username, password, role, first_name, last_name, number_phone, dni)
                        st.success(f"Usuario {first_name} agregado exitosamente")
                        #st.experimental_rerun()
                    else:
                        st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")

        usuarios = user_management.get_users()
        if usuarios:
            df = pd.DataFrame(usuarios)
            df.columns = ['user_id', 'username', 'password', 'role', 'first_name', 'last_name', 'number_phone', 'dni']
            df = df.rename(columns={ 
                'user_id': 'ID',
                'username': 'Nombre de Usuario',
                'password': 'Contraseña',
                'role': 'Rol',
                'first_name': 'Nombres',
                'last_name': 'Apellidos',
                'number_phone': 'Celular',
                'dni': 'DNI',
            })

            # Añadir columna para los botones de editar y eliminar
            def create_buttons(row):
                edit_button = f'<button onclick="window.location.href=\'/?edit={row["Nombre de Usuario"]}\'">✏️</button>'
                delete_button = f'<button onclick="window.location.href=\'/?delete={row["Nombre de Usuario"]}\'">🗑️</button>'
                return edit_button + " " + delete_button

            df['Acciones'] = df.apply(create_buttons, axis=1)

            # Convertir el DataFrame a HTML y mostrarlo
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

            # Manejar edición y eliminación
            query_params = st.query_params
            if 'edit' in query_params:
                selected_user = query_params['edit'][0]
                user = user_management.get_user_by_username(selected_user)
                with st.form("edit_user_form"):
                    new_first_name = st.text_input("Nuevo Nombre", value=user['first_name'])
                    new_last_name = st.text_input("Nuevo Apellido", value=user['last_name'])
                    new_dni = st.text_input("Nuevo DNI", value=user['dni'], max_chars=8)
                    new_number_phone = st.text_input("Nuevo Celular", value=user['number_phone'], max_chars=9)
                    new_role = st.selectbox("Nuevo Rol", ["administrador", "usuario"], index=["administrador", "usuario"].index(user['role']))
                    new_password = st.text_input("Nueva Contraseña", type='password')
                    submit_button = st.form_submit_button("Actualizar Usuario")
            
                    if submit_button:
                        user_management.update_user(
                            user_id=user['user_id'],
                            username=user['username'],
                            password=new_password,
                            role=new_role,
                            first_name=new_first_name,
                            last_name=new_last_name,
                            number_phone=new_number_phone,
                            dni=new_dni
                        )
                        st.success("Usuario actualizado correctamente")
                        st.experimental_set_query_params()
                        st.experimental_rerun()

            if 'delete' in query_params:
                selected_user = query_params['delete'][0]
                user_management.delete_user(selected_user)
                st.success(f"Usuario {selected_user} eliminado exitosamente")
                st.experimental_set_query_params()
                st.experimental_rerun()
        else:
            st.warning("No hay usuarios disponibles para mostrar.")