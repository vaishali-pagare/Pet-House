from django.db import models

# Create your models here.
from AdminApp.models import UserInfo,Pet_Cat

class MyCart(models.Model):
    user = models.ForeignKey(to='AdminApp.UserInfo', on_delete=models.CASCADE)
    pet = models.ForeignKey(to='AdminApp.Pet_Cat',on_delete=models.CASCADE)

    class Meta:
        db_table = "MyCart"
