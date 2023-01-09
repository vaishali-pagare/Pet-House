from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "Category"

class Pets(models.Model):
    pname = models.CharField(max_length=20)
    image = models.ImageField(default='abc,jpg',upload_to='Images')
    section = models.CharField(max_length=20)
    cat = models.ForeignKey(to='Category',on_delete=models.CASCADE)

    class Meta:
        db_table ='Pets'

    def __str__(self):
        return self.pname

class UserInfo(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    username = models.CharField(max_length=20,unique=True)
    pwd = models.CharField(max_length=20)

    class Meta:
        db_table = "UserInfo"

class Pet_Cat(models.Model):
    pet = models.ForeignKey(to='Pets',on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    image = models.ImageField(default='abc.jpg',upload_to='Images')
    price = models.FloatField(default=1000)
    front = models.ImageField(default='abc.jpg',upload_to='Images')
    side = models.ImageField(default='abc.jpg',upload_to='Images')
    description = models.CharField(max_length=200)
    lifespan = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    height = models.CharField(max_length=20)

    class Meta:
        db_table = "Pet_Cat"

class PaymentMaster(models.Model):
    cardno = models.CharField(max_length=20)
    cvv = models.CharField(max_length=20)
    expiry = models.CharField(max_length=20)
    balance = models.IntegerField(default=1000)
    mobile = models.IntegerField(default=111)

    class Meta:
        db_table = "PaymentMaster"

class Appointment(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.IntegerField(default=20)
    address =models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    slottime = models.CharField(max_length=20)
    location =models.CharField(max_length=20)

    class Meta:
        db_table = "Appointment"

class Old_Order(models.Model):
    user = models.ForeignKey(to="AdminApp.UserInfo", on_delete=models.CASCADE)
    amount = models.IntegerField(default=1000)
    dateoforder = models.DateTimeField(default=datetime.datetime.now())
    details = models.CharField(max_length=100)

    class Meta:
        db_table = "Old_Order"


