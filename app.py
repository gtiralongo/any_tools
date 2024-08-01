import streamlit as st
import requests
from requests_html import HTMLSession

# Simulación de credenciales para el ejemplo
credentials = st.secrets["auth"]

# Gestión de estado de la aplicación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Función para obtener el estado de cuenta
def obtener_estado_cuenta():
    # Credenciales de acceso al servicio
    useraysa = st.secrets["auth"]["useraysa"]
    passaysa = st.secrets["auth"]["passaysa"]

    # URL de inicio de sesión
    login_url = "https://acceso.web.aysa.com.ar/saml2/idp/sso/acceso.web.aysa.com.ar"

    with HTMLSession() as session:
        # Enviar la petición de inicio de sesión
        response = session.post(login_url, data={'username': username, 'password': password})
        
        # Verificar si la autenticación fue exitosa
        if response.status_code == 200:
            # Procesar la respuesta para extraer el estado de la cuenta
            cuenta_html = response.html.find('#elemento_estado_cuenta', first=True)
            if cuenta_html:
                return cuenta_html.text
            else:
                return "No se pudo obtener el estado de la cuenta. Verifique sus credenciales."
        else:
            return "Error al intentar iniciar sesión. Código de estado: " + str(response.status_code)

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
    if st.button("Consultar Estado de Cuenta"):
        estado_cuenta = obtener_estado_cuenta()
        st.write(estado_cuenta)
    
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False

# Mostrar la página de inicio de sesión o el panel de administración según el estado de autenticación
if st.session_state.authenticated:
    admin_page()
else:
    login_page()