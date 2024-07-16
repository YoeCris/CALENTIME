import streamlit as st
import pandas as pd
from user_management import UserManagement
from streamlit_option_menu import option_menu
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import bcrypt

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

def validate_dni(dni):
    return len(dni) == 8 and dni.isdigit()

def save_cases_to_file(cases, filename="casos_eliminados.csv"):
    df = pd.DataFrame(cases)
    df.to_csv(filename, index=False)
    return filename

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

st.write(
    """
    <style>
    .header-text {
        font-weight: bold;
        color: #FFD700;  /* Cambia este valor por el color que prefieras */
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
def admin_interface():
    if 'page' not in st.session_state:
        st.session_state.page = 'menu'

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
            st.session_state.page = 'menu'
            st.rerun()

    if main_option == "Visualización" and st.session_state.page == 'menu':
        casos = user_management.get_all_cases()
        users = user_management.get_users()

        if casos:
            df = pd.DataFrame(casos)
            df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'created_date', 'deadline', 'stage']

            st.subheader('Filtros')
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    selected_reviewers = st.multiselect("Filtrar por Encargado", df['reviewer'].unique().tolist(), format_func=lambda x: "Elige una opción" if x == '' else x)
                with col2:
                    selected_stages = st.multiselect("Filtrar por Etapa", df['stage'].unique().tolist(), format_func=lambda x: "Elige una opción" if x == '' else x)

            # Filtrar los datos según las selecciones del usuario
            if selected_reviewers:
                df = df[df['reviewer'].isin(selected_reviewers)]
            if selected_stages:
                df = df[df['stage'].isin(selected_stages)]

            col1, col2 = st.columns(2)

            with col1:
                # Gráfico de distribución de casos por encargado y etapas
                fig2 = px.bar(
                    df, 
                    x='reviewer', 
                    color='stage', 
                    barmode='group', 
                    title='Distribución de Casos por Encargado y Etapa'
                )
                st.plotly_chart(fig2)

                # Gráfico de burbujas para supervisar los casos y encargados
                bubble_df = df.groupby(['reviewer', 'stage']).size().reset_index(name='count')
                fig3 = px.scatter(
                    bubble_df, 
                    x='reviewer', 
                    y='stage', 
                    size='count', 
                    color='stage', 
                    title='Supervisión de Casos por Encargado y Etapa',
                    labels={'count': 'Número de Casos', 'reviewer': 'Encargado', 'stage': 'Etapa'},
                    hover_data={'count': True}
                )
                st.plotly_chart(fig3)

            with col2:
                # Gráfico de casos por estado
                status_counts = df['stage'].value_counts().reset_index()
                status_counts.columns = ['stage', 'count']
                fig4 = px.pie(status_counts, values='count', names='stage', title='Estado de los Casos')
                st.plotly_chart(fig4)

                # Calcular días restantes y colores de semáforo
                df['days_left'], df['total_days'] = zip(*df.apply(lambda row: calculate_days_left(row['created_date'], row['deadline']), axis=1))
                df['semaforo'] = df.apply(lambda row: get_semaforo_color(row['days_left'], row['total_days']), axis=1)

                # Calcular el estado del caso
                df['state'] = df['stage'].apply(lambda x: 'no revisado' if x == 'Preparatoria' else ('en proceso' if x == 'Intermedia' else 'revisado'))
                df_final = df[['semaforo', 'code', 'reviewer', 'stage', 'days_left', 'state']]

                df_final = df_final.rename(
                    columns={
                        'semaforo': '',
                        'code': 'Código',
                        'reviewer': 'Encargado',
                        'stage': 'Etapa',
                        'days_left': 'Faltan',
                        'state': 'Estado'
                    }
                )
                st.subheader("Resumen de Casos")
                st.dataframe(df_final)

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
                ["Modificar Caso", "Agregar Caso"],
                icons=["pencil", "folder-plus"],
                menu_icon="folder",
                default_index=0,
                orientation="horizontal",
            )

        if sub_option == "Modificar Caso" and st.session_state.page == 'menu':
            #st.subheader('Editar o Eliminar')
            casos = user_management.get_all_cases()
            if casos:
                df = pd.DataFrame(casos)
                df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'created_date', 'deadline', 'stage']
                #st.subheader('Filtros')
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        selected_reviewers = st.multiselect("Filtrar por Encargado", df['reviewer'].unique().tolist(), format_func=lambda x: "Elige una opción" if x == '' else x)
                    with col2:
                        selected_stages = st.multiselect("Filtrar por Etapa", df['stage'].unique().tolist(), format_func=lambda x: "Elige una opción" if x == '' else x)


                # Filtrar los datos según las selecciones del usuario
                if selected_reviewers:
                    df = df[df['reviewer'].isin(selected_reviewers)]
                if selected_stages:
                    df = df[df['stage'].isin(selected_stages)]

                cols = st.columns((5, 10, 15, 15, 8, 15, 13, 10, 10, 5, 7))
                headers = ["ID", "Código", "Apellidos", "Nombres", "DNI", "Encargado", "Etapa", "Fecha de Creación", "Fecha de Entrega", "Editar", "Eliminar"]
                for col, header in zip(cols, headers):
                    col.markdown(f"<p class='header-text'>{header}</p>", unsafe_allow_html=True)

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
                    cols = st.columns((5, 10, 15, 15, 8, 15, 13, 10, 10, 5, 7))
                    cols[0].write(f"{row['ID']}", unsafe_allow_html=True)
                    cols[1].write(row['Código'])
                    cols[2].write(row['Apellidos'])
                    cols[3].write(row['Nombres'])
                    cols[4].write(row['DNI'])
                    cols[5].write(row['Encargado'])
                    cols[6].write(row['Etapa'])
                    cols[7].write(f"{row['Fecha de Creación']}", unsafe_allow_html=True)
                    cols[8].write(f"{row['Fecha de Entrega']}", unsafe_allow_html=True)
                    if cols[9].button("✏️", key=f"edit_{row['ID']}"):
                        st.session_state.page = 'edit_case'
                        st.session_state.edit_case = row['ID']
                        st.rerun()
                    if cols[10].button("🗑️", key=f"delete_{row['ID']}"):
                        st.session_state.page = 'confirm_delete_case'
                        st.session_state.delete_case = row['ID']
                        st.rerun()

            else:
                st.warning("No hay casos disponibles para mostrar.")

        elif sub_option == "Agregar Caso" and st.session_state.page == 'menu':
            st.subheader("Agregar Nuevo Caso")
            with st.form("add_case_form"):
                code = st.text_input("Código del Caso")
                investigated_last_name = st.text_input("Apellidos del Investigado")
                investigated_first_name = st.text_input("Nombre del Investigado")
                dni = st.text_input("DNI del Investigado", max_chars=8)
                created_date = st.date_input("Fecha de Creación", value=datetime.date.today())
                deadline = st.date_input("Fecha de Entrega", value=datetime.date.today())

                if not validate_dni(dni):
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
                        st.rerun()

    elif main_option == "Administrar Usuarios":
        sub_option = option_menu(
                "Administrar Usuarios",
                ["Modificar Usuario", "Agregar Usuario"],
                icons=["pencil", "person-plus"],
                menu_icon="person",
                default_index=0,
                orientation="horizontal",
            )

        if sub_option == "Modificar Usuario" and st.session_state.page == 'menu':
            st.subheader("Usuarios")

            usuarios = user_management.get_users()
            if usuarios:
                df = pd.DataFrame(usuarios)
                df.columns = ['user_id', 'username', 'password', 'role', 'first_name', 'last_name', 'number_phone','dni']
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

                cols = st.columns((3, 10, 7, 13, 15, 15, 9, 8, 5, 5))
                headers = ["ID", "Usuario", "Contraseña", "Rol", "Nombres", "Apellidos", "Celular", "DNI", "Editar", "Eliminar"]
                for col, header in zip(cols, headers):
                    col.markdown(f"<p class='header-text'>{header}</p>", unsafe_allow_html=True)


                for i, row in df.iterrows():
                    cols = st.columns((3, 10, 7, 13, 15, 15, 9, 8, 5, 5))
                    cols[0].write(f"{row['ID']}", unsafe_allow_html=True)
                    cols[1].write(row['Nombre de Usuario'])
                    cols[2].write(row['Contraseña'])
                    cols[3].write(row['Rol'])
                    cols[4].write(row['Nombres'])
                    cols[5].write(row['Apellidos'])
                    cols[6].write(row['Celular'])
                    cols[7].write(row['DNI'])
                    if cols[8].button("✏️", key=f"edit_{row['ID']}"):
                        st.session_state.page = 'edit_user'
                        st.session_state.edit_user = row['ID']
                        st.rerun()
                    if cols[9].button("🗑️", key=f"delete_{row['ID']}"):
                        st.session_state.page = 'confirm_delete_user'
                        st.session_state.delete_user = row['ID']
                        st.rerun()

            else:
                st.warning("No hay usuarios disponibles para mostrar.")

        elif sub_option == "Agregar Usuario" and st.session_state.page == 'menu':
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
                    if validate_dni(dni):
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        user_management.create_user(username, hashed_password.decode('utf-8'), role, first_name, last_name, number_phone, dni)
                        st.success(f"Usuario {first_name} agregado exitosamente")
                        st.rerun()
                    else:
                        st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")


    if st.session_state.page == 'edit_case' and 'edit_case' in st.session_state:
        case_id = st.session_state.edit_case
        case = user_management.get_case(case_id)
        st.subheader("Editar Caso")
        with st.form("edit_case_form"):
            code = st.text_input("Código del Caso", value=case.get('code', ''))
            investigated_last_name = st.text_input("Apellidos del Investigado", value=case.get('investigated_last_name', ''))
            investigated_first_name = st.text_input("Nombre del Investigado", value=case.get('investigated_first_name', ''))
            dni = st.text_input("DNI del Investigado", value=case.get('dni', ''), max_chars=8)
            created_date = st.date_input("Fecha de Creación", value=pd.to_datetime(case.get('created_date')))
            deadline = st.date_input("Fecha de entrega", value=pd.to_datetime(case.get('deadline')))
    
            if not validate_dni(dni):
                st.warning("DNI inválido")
                dni = ""
    
            users = user_management.get_users()
            normal_users = [user['first_name'] for user in users if user['role'] == 'usuario']
            reviewer = st.selectbox("Encargado de Revisar el Caso", normal_users, index=normal_users.index(case.get('reviewer', '')))

            stage = st.selectbox("Etapa del Caso", ['Preparatoria', 'Intermedia', 'Juzgamiento'], index=['preparatoria', 'intermedia', 'juzgamiento'].index(case.get('stage', 'preparatoria')))
            edit_case_button = st.form_submit_button("Actualizar Caso")
            cancel_button = st.form_submit_button("Cancelar")

            if edit_case_button and dni:
                user_management.update_case(case['case_id'], code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage)
                st.success(f"Caso {code} actualizado exitosamente")
                del st.session_state['edit_case']
                st.session_state.page = 'menu'
                st.rerun()
            elif cancel_button:
                del st.session_state['edit_case']
                st.session_state.page = 'menu'
                st.rerun()

    if st.session_state.page == 'edit_user' and 'edit_user' in st.session_state:
        user_id = st.session_state.edit_user
        user = user_management.get_user_by_id(user_id)
        st.subheader("Editar Usuario")
        with st.form("edit_user_form"):
            new_first_name = st.text_input("Nuevo Nombre", value=user['first_name'], disabled=True)
            new_last_name = st.text_input("Nuevo Apellido", value=user['last_name'], disabled=True)
            new_dni = st.text_input("Nuevo DNI", value=user['dni'], max_chars=8)
            new_number_phone = st.text_input("Nuevo Celular", value=user['number_phone'], max_chars=9)
            new_role = st.selectbox("Nuevo Rol", ["administrador", "usuario"], index=["administrador", "usuario"].index(user['role']))
            new_password = st.text_input("Nueva Contraseña", type='password')
            submit_button = st.form_submit_button("Actualizar Usuario")
            cancel_button = st.form_submit_button("Cancelar")

            if submit_button:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user_management.update_user(
                    user_id=user['user_id'],
                    username=user['username'],
                    password=hashed_password.decode('utf-8'),
                    role=new_role,
                    first_name=new_first_name,
                    last_name=new_last_name,
                    number_phone=new_number_phone,
                    dni=new_dni
                )
                st.success("Usuario actualizado correctamente")
                del st.session_state['edit_user']
                st.session_state.page = 'menu'
                st.rerun()
            elif cancel_button:
                del st.session_state['edit_user']
                st.session_state.page = 'menu'
                st.rerun()

    if st.session_state.page == 'confirm_delete_case' and 'delete_case' in st.session_state:
        case_id = st.session_state.delete_case
        case = user_management.get_case(case_id)
        st.subheader("Confirmar Eliminación de Caso")
        st.write("¿Está seguro de que desea eliminar el siguiente caso?")
        df = pd.DataFrame([case])
        st.dataframe(df)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Eliminar Caso"):
                user_management.delete_case(case_id)
                st.success(f"Caso con ID {case_id} eliminado exitosamente")
                del st.session_state['delete_case']
                st.session_state.page = 'menu'
                st.rerun()
        with col2:
            if st.button("Cancelar"):
                del st.session_state['delete_case']
                st.session_state.page = 'menu'
                st.rerun()

    if st.session_state.page == 'confirm_delete_user' and 'delete_user' in st.session_state:
        user_id = st.session_state.delete_user
        user = user_management.get_user_by_id(user_id)
        affected_cases = user_management.get_cases_by_reviewer(user['first_name'])
        st.subheader("Confirmar Eliminación de Usuario")
        st.write("¿Está seguro de que desea eliminar el siguiente usuario?")
        df_user = pd.DataFrame([user])
        st.dataframe(df_user)
        st.write("Casos afectados:")
        df_cases = pd.DataFrame(affected_cases)
        st.dataframe(df_cases)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Guardar Casos Afectados"):
                filename = save_cases_to_file(affected_cases)
                st.success(f"Casos afectados guardados en {filename}")
        with col2:
            if st.button("Eliminar Usuario y Casos"):
                user_management.delete_user_and_cases(user_id)
                st.success(f"Usuario con ID {user_id} y sus casos eliminados exitosamente")
                del st.session_state['delete_user']
                st.session_state.page = 'menu'
                st.rerun()
        with col3:
            if st.button("Cancelar"):
                del st.session_state['delete_user']
                st.session_state.page = 'menu'
                st.rerun()

