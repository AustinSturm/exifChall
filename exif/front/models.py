from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
class images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ifile = models.FileField(upload_to='media/')
    rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
