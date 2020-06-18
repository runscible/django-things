from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.test import TestCase

from rest_framework import status 
from rest_framework.test import APIClient

from core.models import Tag 

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTest(TestCase):
    """test the public tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login(self):
        """test the login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) 

class PrivateTagsApiTest(TestCase):
    """test the private tags api"""              

    def setUp(self):
        self.user = get_user_model()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        """test retrieving tags"""
        Tag.objects.create(user=self.user, name='carpentry')
        Tag.objects.create(user=self.user, name='blacksmithing')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')

        serializer = TagsSerilizer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test that tags returned only are for the authenticated user"""

        user_2 = get_user_model().objects.create(
            'user_2@testcase.com',
            'testpassword_2'
        )    

        Tags.objects.create(user=user_2, name='show')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        