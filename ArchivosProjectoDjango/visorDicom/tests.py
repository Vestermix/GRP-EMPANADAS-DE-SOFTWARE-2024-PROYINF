from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):

    def setUp(self):
        # Crea un usuario de prueba antes de cada prueba
        self.username = 'testuser'
        self.password = 'password123'
        self.email = 'testuser@example.com'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_successful(self):
        # Intenta iniciar sesión con credenciales correctas
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login exitoso', response.content)  # Cambia esto según lo que retorne tu vista

        # Verificar que el último inicio de sesión se actualiza
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login)

    def test_login_failed_wrong_password(self):
        # Intenta iniciar sesión con una contraseña incorrecta
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Contraseña incorrecta', response.content)

    def test_login_failed_user_not_exist(self):
        # Intenta iniciar sesión con un usuario no existente
        response = self.client.post(reverse('login'), {
            'username': 'nonexistentuser',
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario no existe', response.content)

    def test_registration_successful(self):
        # Registra un nuevo usuario
        response = self.client.post(reverse('formulario'), {
            'username': 'newuser',  # Asegúrate de que este nombre de usuario no exista
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario creado correctamente', response.content)

        # Verificar que el nuevo usuario ha sido creado
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_failed_duplicate_username(self):
        # Intenta registrar un usuario con el mismo nombre de usuario
        response = self.client.post(reverse('formulario'), {
            'username': self.username,  # Usa el mismo nombre de usuario que ya existe
            'email': 'duplicate@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('El usuario o correo ya existe', response.content)

    def test_registration_failed_password_mismatch(self):
        # Intenta registrar un usuario con contraseñas que no coinciden
        response = self.client.post(reverse('formulario'), {
            'username': 'mismatcheduser',
            'email': 'mismatched@example.com',
            'password1': 'password123',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Las contraseñas no coinciden', response.content)

