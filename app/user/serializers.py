from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _ 


class UserSerializer(serializers.ModelSerializer):
    """serializer for the users model"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'pasword': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create new user with created password"""
        return get_user_model().objects.create_user(**validated_data)    
class AuthTokenSerializer(serializers.Serializer):
    """serializers for user authentication token"""
    email = serializers.CharField()
    password = serializers.CharField( 
            style = {'input_type': 'password'},
            trim_whitespace = False )
    
    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('unable to athenticate whith the provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs