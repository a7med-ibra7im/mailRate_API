from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from .models import Meal,Rating
from .serializers import *

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            """
            create or update
            """
            meal=Meal.objects.get(id=pk)
            username=request.data['username']
            user=User.objects.get(username=username)
            stars=request.data['stars']
            
            try:
                rating =Rating.objects.get(user=user.id,meal=meal.id)
                rating.stars = stars
                rating.save()
                serializer = MealSerializer(rating,many=False)
                json = {
                        'message': 'Meal Rate Updated.',
                        'result': serializer.data
                    }
                return Response(json, status=status.HTTP_200_OK)
                
            except:
                rate = Rating.objects.create(user=user,meal=meal,stars=stars)
                serializer = MealSerializer(rate,many=False)
                json = {
                    'message': 'Meal Rate Created',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_200_OK)


                
                
        else:
            return Response({'message': 'Stars Not Provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    