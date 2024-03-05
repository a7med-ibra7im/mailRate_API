from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from .models import Meal,Rating
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                'token': token.key, 
                }, 
            status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            """
            create or update
            """
            meal=Meal.objects.get(id=pk)
            user = request.user
            # username=request.data['username']
            # user=User.objects.get(username=username)
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
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated)
    
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)