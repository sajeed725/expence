from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Category(models.Model):

    name=models.CharField(max_length=200)

    budget=models.PositiveIntegerField()

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    image=models.ImageField(upload_to="cat_images",default="/cat_images/default.jpeg")

    class Meta:

        unique_together=("name","owner")

    def __str__(self):

       return self.name


class Transactions(models.Model):

    title=models.CharField(max_length=200)

    amount=models.PositiveIntegerField()

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)

    payment_options=(
        ("cash","cash"),
        ("upi","upi"),
        ("card","card")
    )

    payment_method=models.CharField(max_length=200,choices=payment_options,default="cash")

    created_date=models.DateTimeField(auto_now_add=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):

        return self.title
