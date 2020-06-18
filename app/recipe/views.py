from rest_framework import viewsets, mixins 
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated 

from core.models import Tag 
from recipe import serializers 


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """"manage tags in the database"""
    classes_authentication = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

