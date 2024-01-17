from django.db import models

# Create your models here.
class custommanager(models.Manager):
    
    def get_pet_age(self):
        # return super().get_queryset().filter(Age=1)
        # return super().get_queryset().order_by(Age)
        return super().get_queryset().filter(Breed='labra')

class pet(models.Model):
    gender=(('male','Male'),('female','Female'))
    Image=models.ImageField(upload_to='media')
    Name=models.CharField(max_length=200)
    Species=models.CharField(max_length=200)
    Breed=models.CharField(max_length=200)
    Age=models.IntegerField()
    Gender=models.CharField(max_length=100,choices=gender)
    Description=models.CharField(max_length=200)
    Price=models.IntegerField()
    slug=models.SlugField(default='',null=False)

    # objects=Manager()
    # here object manager class ka hota hai or
    #  niche pets objects banaya humne customemanager class ka
# custommanager class child class hai manager class ka
    pets=custommanager()
    class Meta:
        db_table='pet'

class user(models.Model):
    gender=(('male','Male'),('female','Female'))
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    password=models.CharField(max_length=200,default='')
    confirmpassword=models.CharField(max_length=120 ,default='')
    Gender=models.CharField(max_length=200,choices=gender)
    contact=models.BigIntegerField()
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.IntegerField()
    
    

    class Meta:
        db_table='user'

class cart(models.Model):
    productid=models.ForeignKey(pet,on_delete=models.CASCADE)
    customerid=models.ForeignKey(user,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    Totalamt=models.FloatField()

    class Meta:
        db_table='cart'


class order(models.Model):
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    address=models.CharField(max_length=200)
    contact=models.BigIntegerField()
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.IntegerField()
    ordernumber=models.CharField(max_length=100)
    totalbillamount=models.FloatField(default=0)

    class Meta:
        db_table='order'

class payment(models.Model):
    customerid=models.ForeignKey(user,on_delete=models.CASCADE)
    oid=models.ForeignKey(order,on_delete=models.CASCADE)
    paymentstatus=models.CharField(max_length=100,default='pending')
    trasactionid=models.CharField(max_length=200)
    paymentmode=models.CharField(max_length=100,default='paypal')

    class Meta:
        db_table='payment'

class orderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(user,on_delete=models.CASCADE)
    productid=models.ForeignKey(pet,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE,null=True,default=0)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='oderdetail'



