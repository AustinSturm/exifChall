from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

def upld_dir(instance, filename):
    return 'user-{0}/{1}'.format(instance.user.id, filename)

class images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ifile = models.ImageField(upload_to=upld_dir)
    rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
