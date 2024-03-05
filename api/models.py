from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    
    def no_of_ratings(self):
        rating=Rating.objects.filter(meal=self)
        return len(rating)
        
    def avg_rating(self):
        rating=Rating.objects.filter(meal=self)
        sum=0
        
        for x in rating:
            sum += x.stars
        if len(rating) > 0 :
            return sum/len(rating)
        else:
            return 0
    

    def __str__(self):
        return self.title
    
    


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} - {self.meal.title}"


    class Meta:
        unique_together = (('user', 'meal'),)
        index_together = (('user', 'meal'),)
