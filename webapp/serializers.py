from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note  # Указываем модель, которую будем сериализовать
        fields = ['id', 'title', 'content', 'created_at']
