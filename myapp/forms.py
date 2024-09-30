from typing import Any
from django import forms

from myapp.models import Category,Transactions

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class CatogaryForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):

        self.user=kwargs.pop("user")

        return super().__init__(*args,**kwargs)

    class Meta:

        model = Category

        fields = ['name','budget','image']

        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),

            "budget":forms.NumberInput(attrs={"class":"form-control"}),

            "image":forms.FileInput(attrs={"class":"form-control"}),

           
        }

    def clean(self):

        self.cleaned_data=super().clean()

        print(self.user,"inside cat form----")

        budget_amount=int(self.cleaned_data.get("budget"))

        if budget_amount<100:

            print("budget amount should be graeter than 100")
            
            self.add_error("budget","budget amount > 100")

        category_name=self.cleaned_data.get("name")

        owner=self.user

        if not self.instance.pk:
            print("updating",self.instance.pk)

            is_exist=Category.objects.filter(name__iexact=category_name,owner=owner).exists()

            if is_exist:

                self.add_error("name","already exist")

        else:

            is_exist = Category.objects.filter(name__iexact=category_name,owner=owner).exclude(pk=self.instance.pk).exists()     

        return self.cleaned_data


class TransactionForm(forms.ModelForm):

    class Meta:

        model =  Transactions

        fields = ['title','amount','category_object','payment_method']       

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),

            "amount":forms.NumberInput(attrs={"class":"form-control mb-2"}),

            "category_object":forms.Select(attrs={"class":"form-control mb-2"}),

            "payment_method":forms.Select(attrs={"class":"form-control mb-2"}),

           

        }


class TransactionFilterForm(forms.Form):

    start_date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))

    end_date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))



class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput (attrs={"class":"form-control mb-2"}))
    password2=forms.CharField(widget=forms.PasswordInput (attrs={"class":"form-control mb-2"}))

    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={

            "username":forms.TextInput(attrs={"class":"form-control mb-2"}),
            "email":forms.EmailInput(attrs={"class":"form-control mb-2"})

        }


class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-3"}))


    
            