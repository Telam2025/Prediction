from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    SEXE_CHOICES = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    ville = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()

        img=Image.open(self.image.path)

        if img.height >300 or img.width>300:
         output_size=(300,300)
         img.thumbnail(output_size)
         img.save(self.image.path)
