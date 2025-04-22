from django.db import models

class ContactStatusChoices(models.Model):
    status = models.CharField(primary_key=True, max_length=300, unique=True)

    def __str__(self):
        return self.status

class Contact(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=300)
    status = models.ForeignKey(ContactStatusChoices, related_name='contacts', null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.email