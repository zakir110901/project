from django.db import models

# Create your models here.
STATE_CHOICE = (
    ('Participation','Participation'),
    ('Winner','Winner')
)

class db(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    state = models.CharField(max_length=20, choices=STATE_CHOICE, default='participation')

    def __str__(self):
        return self.name
    
class pdf(models.Model):
    pdf = models.FileField(upload_to='uploads/')