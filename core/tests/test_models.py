from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    """Test creating a new user with email is successful"""

    def test_create_user(self):

        email = 'kishan@django.com'
        password = 'kishan123'

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Check email is normalized"""

        email = 'kishan@DJANGO.COM'
        user = get_user_model().objects.create_user(email,'test123')

        self.assertEqual(user.email,email.lower())

    def test_new_user_with_no_email(self):

        """test creating a new user with empty email address"""

        with self.assertRaises(ValueError):

            get_user_model().objects.create_user(None,'test123')


    def test_create_new_superuser(self):
        """test creating a new super user"""

        user = get_user_model().objects.create_superuser('kishan@django.com','test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)