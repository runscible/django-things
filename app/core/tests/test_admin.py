from django.test import TestCase, Client 
from django.contrib.auth import get_user_model 
from django.urls import reverse 


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'email@mail.com',
            password = 'password123'
        )
        self.client.force_login(self.admin_user)

    def test_users_listed(self):
        """test users listed in one page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.admin_user.name)
        self.assertContains(res, self.admin_user.email)

    def user_page_change(self):
        """check if the user edit page works correctly"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url) 
        self.assertEqual(res.status_code, 200)   

    def test_create_user_page(self):
        """test if the create user page is created"""    
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)