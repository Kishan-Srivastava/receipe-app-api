from xml.dom import ValidationErr
from rest_framework import serializers
#from django.utils.translation import ugettext_lazy as _


from django.contrib.auth import get_user_model,authenticate

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id','email','password','name']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'min_length':5,
                'style':{'input_type':'password'}
            }
        }

    
    def create(self,validated_data):

        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password',None)

        user = super().update(instance,validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class UserAuthTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False)

    def validate(self,attrs):

        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('email'),
            password = attrs.get('password')
        )

        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs

# class UserManagerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = get_user_model()
#         fields = ['email','name','password']
#         extra_kwargs = {
#             'password':{
#                 'style':{'input_type':'password'},
#                 'write_only':True
#             }
#         }
