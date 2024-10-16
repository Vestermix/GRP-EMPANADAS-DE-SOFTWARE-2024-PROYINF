import unittest
import requests
from bs4 import BeautifulSoup

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:8000"
        cls.login_url = f"{cls.base_url}/login/"
        cls.session = requests.Session()

    def get_csrf_token(self, url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    def test_login_exitoso(self):
        # Obtener el token CSRF
        csrf_token = self.get_csrf_token(self.login_url)
        login_data = {
            "username": "h",
            "password": "h",
            "csrfmiddlewaretoken": csrf_token
        }

        # Probar login exitoso con credenciales válidas
        response = self.session.post(self.login_url, data=login_data, allow_redirects=False)
        self.assertEqual(response.status_code, 302)  # Redirección exitosa

    def test_login_fallido(self):
        # Obtener el token CSRF
        csrf_token = self.get_csrf_token(self.login_url)
        login_data = {
            "username": "h",
            "password": "incorrecto",
            "csrfmiddlewaretoken": csrf_token
        }

        # Probar login fallido con contraseña incorrecta
        response = self.session.post(self.login_url, data=login_data)
        self.assertIn("Contraseña incorrecta", response.text)

class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:8000"
        cls.register_url = f"{cls.base_url}/formulario/"
        cls.session = requests.Session()

    def get_csrf_token(self, url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    def test_registro_exitoso(self):
        # Obtener el token CSRF
        csrf_token = self.get_csrf_token(self.register_url)
        valid_registration = {
            "username": "v",
            "email": "v@v",
            "password1": "v",
            "password2": "v",
            "csrfmiddlewaretoken": csrf_token
        }

        # Probar registro exitoso con datos válidos
        response = self.session.post(self.register_url, data=valid_registration, allow_redirects=False)
        self.assertEqual(response.status_code, 302)  # Redirección exitosa


    def test_registro_usuario_existente(self):
        # Obtener el token CSRF
        csrf_token = self.get_csrf_token(self.register_url)
        existing_user_registration = {
            "username": "h",
            "email": "h@h",
            "password1": "h",
            "password2": "h",
            "csrfmiddlewaretoken": csrf_token
        }

        # Probar registro con un usuario que ya existe
        response = self.session.post(self.register_url, data=existing_user_registration)
        self.assertEqual(response.status_code, 200)
