from django.db import models
from django.utils import timezone

# Create your models here.

class TaakVarity(models.Model):
    TAAK_TYPE_CHOICE =[
        ('ML','MASALA'),
        ('GR','GINGER'),
        ('KL','KIWI'),
        ('PL','PLAIN'),
        ('EL','ELAICHI'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='taak/')
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=TAAK_TYPE_CHOICE)
    description = models.TextField(default='')

    def __str__(self):
        return self.name