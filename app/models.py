
from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# from django.core.validators import MaxValueValidator, MinValueValidator

class Color(models.Model):
    name = models.CharField(max_length=255)
    code= models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    name = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name

class FilterYear(models.Model):  # Changed to follow naming conventions
    FILTER_YEAR = (
        ("1990 TO 2000", "1990 TO 2000"),
        ('2000 TO 2010', "2000 TO 2010"),
        ('2010 TO 2020', "2010 TO 2020"),
    )

    def __str__(self):
        return self.year
    
    year = models.CharField(choices=FILTER_YEAR, max_length=60)

class Product(models.Model):
    CONDITIONS = (("NEW", "NEW"), ("OLD", "OLD"))
    STOCK = (("IN STOCK", "IN STOCK"), ('OUT OF STOCK', 'OUT OF STOCK'))
    STATUS = (("PUBLIC", "PUBLIC"), ("DRAFT", "DRAFT"))

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(choices=CONDITIONS, max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_year = models.ForeignKey(FilterYear, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime("%Y%m%d")+str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Images(models.Model):
    image=models.ImageField(upload_to='products/')
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)

    

class Tag(models.Model):
    name=models.CharField(max_length=200)
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Contact_us(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField(null=True)
    phone = models.IntegerField()
    email = models.EmailField( max_length=100)
   
    amount = models.CharField(max_length=100)
    # payment_id = models.CharField(max_length=300,null=True,blank=True)
    # paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField( max_length=200)
    image = models.ImageField( upload_to='products/Order_Img')
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username
    

    

   