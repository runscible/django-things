from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse 

from rest_framework.test import APIClient 
from rest_framework import status 


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the public user api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test that check if a valid user has created"""
        payload = {
            'email': 'test@holatest.com',
            'password': 'testpass123',
            'name': 'john test'
        }    

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_user_exists(self):
        """test case for created user"""
        payload = {
            'email': 'test@holatest.com',
            'password': 'testpass123'
        }    
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



    def test_password_too_short(self):
        """check the password length must be longer than 5"""
        payload = {
            'email': 'test@holatest.com',
            'password': '123'
        }    
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email'],
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self): 
        """test for created token for user"""
        payload = { 'email': 'test@holatest.com', 'password': 'testpass123',}   
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """test case for invalid credentials for token"""
        create_user(email='test@holatest.com', password='testpass123')
        payload = {
            'email': 'test@holatest.com',
            'password': 'culo.'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_not_user(self):
        """test that are no token created if the user not exists"""
        payload = {
            'email': 'test@holatest.com',
            'password': 'testpass123'
        }    

        res = self.client.post(TOKEN_URL, payload) 
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing(self):
        """"test email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': '', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)        