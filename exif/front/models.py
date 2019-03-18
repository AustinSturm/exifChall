from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
from exif.settings import MEDIA_ROOT

def upld_dir(instance, filename):
    return 'user-{0}/{1}'.format(instance.user.id, uuid4())

class images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(default="image", max_length=60, blank=False)
    ifile = models.ImageField(unique=True, upload_to=upld_dir)
    rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def get_upldName(self):
        return self.ifile.name.split('/')[-1]

    def get_renderUrl(self):
        return None
