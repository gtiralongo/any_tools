import streamlit as st
from requests_html import HTMLSession

# Simulación de credenciales para el ejemplo
credentials = st.secrets["auth"]

# Gestión de estado de la aplicación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Función para obtener el estado de cuenta utilizando requests-html
def obtener_estado_cuenta(username, password):
    try:
        session = HTMLSession()
        login_url = "https://acceso.web.aysa.com.ar/saml2/idp/sso/acceso.web.aysa.com.ar"
        login_data = {
            'username': username,
            'password': password
        }
        
        response = session.post(login_url, data=login_data)
        
        if response.status_code == 200:
            # Ajustar selector según el contenido real de la página
            estado_cuenta = response.html.find('#elemento_estado_cuenta', first=True)
            if estado_cuenta:
                return estado_cuenta.text
            else:
                return "No se pudo obtener el estado de la cuenta."
        else:
            return f"Error al intentar iniciar sesión. Código de estado: {response.status_code}"
    except Exception as e:
        return f"Error al obtener el estado de la cuenta: {e}"

# Página de Inicio de Sesión
def login_page():
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Iniciar sesión")
    
    if login_button:
        if username in credentials and credentials[username] == password:
            st.session_state.authenticated = True
        else:
            st.error("Usuario o contraseña incorrectos")

# Pantalla de Administración
def admin_page():
    st.title("Panel de Administración")
    st.write("¡Bienvenido, administrador!")
    
    # Ejemplo de opciones en el panel de administración
    tab1, tab2, tab3 = st.tabs(["Aysa", "Metrogas", "Edenor"])

    with tab1:
        st.write("Aysa")
        if st.button("Consultar Estado de Cuenta Aysa"):
            # Usar las credenciales de la cuenta para iniciar sesión y obtener datos
            username = st.secrets["account"]["useraysa"]
            password = st.secrets["account"]["passaysa"]
            estado_cuenta = obtener_estado_cuenta(username, password)
            st.write(estado_cuenta)
    
    with tab2:
        st.write("Metrogas")

    with tab3:
        st.write("Edenor")
    
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False

# Mostrar la página de inicio de sesión o el panel de administración según el estado de autenticación
if st.session_state.authenticated:
    admin_page()
else:
    login_page()