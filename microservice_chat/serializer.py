from microservice_chat.models import User, ChatMessage, Profile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id_origin', 'name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id_origin', 'name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create(
            id_origin = validated_data['id_origin'],
            name=validated_data['name'],
            last_name=validated_data['last_name']

        )

        #user.set_password(validated_data['password'])
        user.save()

        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [ 'id',  'user',  'full_name', 'image' ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class MessageSerializer(serializers.ModelSerializer):
    reciever_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id','sender', 'receiver', 'reciever_profile', 'sender_profile' ,'message', 'is_read', 'date']
    
    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2