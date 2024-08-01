import streamlit as st
import requests
from requests_html import HTMLSession

# Leer credenciales desde secrets.toml
username = st.secrets["auth"]["username"]
password = st.secrets["auth"]["password"]

# URL de inicio de sesión
login_url = "https://acceso.web.aysa.com.ar/saml2/idp/sso/acceso.web.aysa.com.ar"

# Función para iniciar sesión y obtener datos
def obtener_estado_cuenta():
    with HTMLSession() as session:
        # Enviar la petición de inicio de sesión
        response = session.post(login_url, data={'username': username, 'password': password})
        
        # Verificar si la autenticación fue exitosa
        if response.status_code == 200:
            # Procesar la respuesta para extraer el estado de la cuenta
            # Ajusta esto basado en la estructura de la página después de iniciar sesión
            cuenta_html = response.html.find('#elemento_estado_cuenta', first=True)
            if cuenta_html:
                return cuenta_html.text
            else:
                return "No se pudo obtener el estado de la cuenta. Verifique sus credenciales."
        else:
            return "Error al intentar iniciar sesión. Código de estado: " + str(response.status_code)

# Interfaz de usuario de Streamlit
st.title("Consulta de Estado de Cuenta")

if st.button("Consultar Estado de Cuenta"):
    estado_cuenta = obtener_estado_cuenta()
    st.write(estado_cuenta)