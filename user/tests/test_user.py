from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_AUTH_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """test for creating a user"""
        payload = {
            'email':'kishan@django.com',
            'password':'kishan333',
            'name':'kishan'
        }
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertTrue(user)
        self.assertNotIn('password',res.data)

    def test_user_exists(self):
        """test for if user is already exsists"""

        payload = {
            'email':'Kishan@django.com',
            'password':'kishan333',
            'name':'Kishan'
        }
        user = create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test for password of length less than 5 characters"""

        payload = {
            'email':'kishan@django.com',
            'password':'pw',
            'name':'Kishan',
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_token_created(self):
        """Test to create auth token"""
        payload = {'email':'kishan@django.com','password':'kishan333','name':'kishan'}
        user = create_user(**payload)
        res = self.client.post(CREATE_AUTH_TOKEN_URL,{'email':'kishan@django.com','password':'kishan333'})

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('token',res.data)

    def test_create_token_for_wrong_credentials(self):

        """test to check when user logged in using wrong credentials"""
        payload = {'email':'kishan@django.com','password':'kishan333','name':'kishan'}
        user = create_user(**payload)
        res = self.client.post(CREATE_AUTH_TOKEN_URL,{'email':'kishan@django.com','password':'wrong'})

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token',res.data)

    def test_create_token_no_user(self):
        """test to create token that does not exists"""

        res = self.client.post(CREATE_AUTH_TOKEN_URL,{'email':'kishan@django.com','password':'kishan'})

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(CREATE_AUTH_TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_unauthorised_user_access_to_me_url(self):

        """test to check unauthorised access to me url"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPICase(TestCase):

    def setUp(self):
        payload = {
                'email':'test@django.com',
                'password':'test123',
                'name':'Test'
            }
        self.user = get_user_model().objects.create_user(**payload)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    
    def test_user_authorize_to_access_me_url(self):

        """test to check whether user can access me url"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['email'],self.user.email)

    def test_post_method_not_allowed(self):

        """test for post method to me url"""

        res = self.client.post(ME_URL,{})

        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_updated_successfully(self):
        """test to update user"""
        payload = {
            'email':'kishan@django.com'
        }

        res = self.client.patch(ME_URL,payload)

        self.assertEqual(res.data['email'],'kishan@django.com')
        self.assertEqual(res.status_code,status.HTTP_200_OK)


