from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    
    def test_user_with_email_successfull(self):
        """ test for a new user with a successfull email """
        email = "test@test.com"
        password = "Test123"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ test the mail for a new user is normalized """
        email = 'test@Ttest.com'
        user = get_user_model().objects.create_user(email, 'test123')
        
        self.assertEqual(user.email, email.lower())

    def test_new_user_valid_email(self):
        """ test for check if created user has a valid email """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')     


    def test_super_user_created(self):
        """" test super user created """
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
