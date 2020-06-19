from django.contrib.auth import get_user_model 
from django.urls import reverse 
from django.test import TestCase

from rest_framework import status 
from rest_framework.test import APIClient 

from core.models import Tag 

from recipe.serializers import TagSerializer 

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    """test the publicity on the available tags"""

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)    

class PrivateTagsAPiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
          'test@holatest.com',
          'testpass123'
        )
        self.client.force_authenticate(self.user) 

    def test_retrieve_tags(self):
        """test retrieving tags"""           
        Tag.objects.create(user=self.user, name='cars')
        Tag.objects.create(user=self.user, name='artistic')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_tags_limited_to_user(self):
        """test number of tags returned for a user"""
        user_2 = get_user_model().objects.create_user(
            "test_2@testcase.com",
            "testpassword2"
        )    

        Tag.objects.create(user=user_2, name='food')
        tag = Tag.objects.create(user=self.user, name='electronics')

        res = self.client.get(TAGS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

        
