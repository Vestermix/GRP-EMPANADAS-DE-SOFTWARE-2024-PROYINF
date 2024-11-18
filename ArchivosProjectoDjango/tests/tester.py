import unittest
import requests

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "https://api.example.com"
        cls.login_url = f"{cls.base_url}/login"
        cls.register_url = f"{cls.base_url}/register"
        
        cls.valid_login = {"username": "user", "password": "password123"}
        cls.invalid_login = {"username": "user", "password": "wrong_password"}
        cls.valid_registration = {
            "username": "new_user", 
            "password": "new_password123", 
            "email": "new_user@example.com"
        }
        cls.existing_user_registration = {
            "username": "user", 
            "password": "password123", 
            "email": "user@example.com"
        }

    def test_login_exitoso(self):
        # Probar login exitoso con credenciales válidas
        response = requests.post(self.login_url, json=self.valid_login)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())  # Verifica que se devuelva un token
        self.assertEqual(response.json()["message"], "Login exitoso")

    def test_login_no_exitoso(self):
        # Probar login no exitoso con credenciales incorrectas
        response = requests.post(self.login_url, json=self.invalid_login)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Credenciales incorrectas")


class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "https://api.example.com"
        cls.register_url = f"{cls.base_url}/register"
        
    def test_registro_exitoso(self):
        # Probar registro exitoso con datos válidos
        response = requests.post(self.register_url, json=self.valid_registration)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Usuario registrado exitosamente")

    def test_registro_no_exitoso(self):
        # Probar registro no exitoso cuando el usuario ya existe
        response = requests.post(self.register_url, json=self.existing_user_registration)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "El usuario ya existe")

    @classmethod
    def tearDownClass(cls): #se supone que esta linea debe destruir el usuario creado en el test_registro_exitoso, sin embargo hay que desarrollar este punto y verificar su funcionamiento
        pass

if __name__ == '__main__':
    unittest.main()

