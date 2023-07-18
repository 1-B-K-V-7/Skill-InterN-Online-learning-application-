from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    description = models.TextField(max_length=250)

    def __str__(self):      # dunter method in python ......refer more  To show name in Contacts database details in admin
        return self.name
