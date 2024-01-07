from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class addfishcategory(models.Model):
    name = models.CharField(max_length=200,null=True,blank=False)
    description = models.CharField(max_length=200,null=True,blank=False)
    image = models.ImageField(upload_to='image',null=True,blank=False)


class addfishdetatls(models.Model):
    fishcategory = models.CharField(max_length=200, null=True, blank=False)
    proname = models.CharField(max_length=200, null=True, blank=False)
    proqty = models.IntegerField(null=True, blank=False)
    proprice = models.IntegerField( null=True, blank=False)
    image = models.ImageField(upload_to='image', null=True, blank=False)

class saveuser(models.Model):
    fname = models.CharField(max_length=200, null=True, blank=False)
    lname = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200,null=True, blank=False)
    password = models.CharField(max_length=200, null=True, blank=False)

class Fwcart(models.Model):
    productid = models.ForeignKey(addfishdetatls,on_delete=CASCADE,null=True,blank=True)
    userid = models.ForeignKey(saveuser,on_delete=CASCADE,null=True,blank=False)
    total = models.IntegerField(null=True,blank=False)
    quantity = models.IntegerField(null=True,blank=False)
    status = models.IntegerField(null=True,blank=False)

class checkoutdet(models.Model):
    cartid = models.ForeignKey(Fwcart,on_delete=CASCADE,null=True,blank=True)
    finame = models.CharField(max_length=200, null=True, blank=False)
    lname = models.CharField(max_length=200, null=True, blank=False)
    uname = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    add1 = models.CharField(max_length=200, null=True, blank=False)
    add2 = models.CharField(max_length=200, null=True, blank=False)
    country = models.CharField(max_length=200, null=True, blank=False)
    state = models.CharField(max_length=200, null=True, blank=False)
    zip = models.CharField(max_length=200, null=True, blank=False)
    shippingmethod = models.CharField(max_length=200, null=True, blank=False)


class savecontactdata(models.Model):
    fname = models.CharField(max_length=200,null=True,blank=False)
    email = models.CharField(max_length=200,null=True,blank=False)
    msg = models.CharField(max_length=200,null=True,blank=False)
    sub = models.CharField(max_length=200,null=True,blank=False)

class shippingaddress(models.Model):
    finame = models.CharField(max_length=200, null=True, blank=False)
    lname = models.CharField(max_length=200, null=True, blank=False)
    uname = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    add1 = models.CharField(max_length=200, null=True, blank=False)
    add2 = models.CharField(max_length=200, null=True, blank=False)
    country = models.CharField(max_length=200, null=True, blank=False)
    state = models.CharField(max_length=200, null=True, blank=False)
    zip = models.CharField(max_length=200, null=True, blank=False)
    paymenttype = models.CharField(max_length=200, null=True, blank=False)
    shippingmethod = models.CharField(max_length=200, null=True, blank=False)

