from rest_framework import serializers
from .models import Meal,Rating
from django.contrib.auth.models import User

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'meal', 'stars']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'title', 'description']
