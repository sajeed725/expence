from django.shortcuts import render,redirect

from myapp.forms import CatogaryForm,TransactionForm,TransactionFilterForm,RegistrationForm,LoginForm

from django.views.generic import View

from myapp.models import Category,Transactions

from django.utils import timezone

from django.db.models import Sum,Avg,Count,Min,Max

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator


@method_decorator(signin_required,name="dispatch")
class CategoryCreateView(View):
    
    def get(self,request,*args,**kwargs):

        # if not request.user.is_authenticated:
        #     messages.error(request,"invalid session plz signin")
        #     return redirect("signin")

        form_instance=CatogaryForm(user=request.user)

        qs=Category.objects.filter(owner=request.user)

        return render(request,"category_form.html",{"form":form_instance,"Categories":qs})
    
    def post(self,request,*args,**kwargs):

        # if not request.user.is_authenticated:
        #     messages.error(request,"invalid session plz signin")
        #     return redirect("signin")

        form_instance=CatogaryForm(request.POST,user=request.user,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            # data=form_instance.cleaned_data

            # Category.objects.create(**data,owner=request.user)

            return redirect("category-add")
        else:
            return render(request,"category_form.html",{"form":form_instance})
    

@method_decorator(signin_required,name="dispatch")
class CategoryUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        form_instance=CatogaryForm()

        category_object=Category.objects.get(id=id)

        form_instance=CatogaryForm(instance=category_object)

        return render(request,"category_edit.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk") 

        form_instance=CatogaryForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            Category.objects.filter(id=id).update(**data)

            return redirect("category-add")
        else:
             return render(request,"category_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionForm()

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        categories=Category.objects.filter(owner=request.user)

        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)

        return render(request,'transaction_add.html',{"form":form_instance,"transactions":qs,"categories":categories})
    
    def post(self,request,*args,**kwargs):

        form_instance=TransactionForm(request.POST)

        if form_instance.is_valid():
            
            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("transaction-add")
        else:
            return render(request,'transaction_add.html',{"form":form_instance})


# url:lh:8000/transaction/{int:pk}/change/
@method_decorator(signin_required,name="dispatch")
class TransactionUpdateView(View):

     def get(self,request,*args,**kwargs):
         
         id=kwargs.get("pk")

         trans_object=Transactions.objects.get(id=id)

         form_instance=TransactionForm(instance=trans_object)

         return render(request,"transaction_edit.html",{"form":form_instance})
     
     def post(self,request,*args,**kwargs):
         
         id=kwargs.get("pk")

         trans_object=Transactions.objects.get(id=id)

         form_instance=TransactionForm(request.POST,instance=trans_object)

         if form_instance.is_valid():

            form_instance.save()

            return redirect("transaction-add")
         else:
            return render(request,"transaction_edit.html",{"form":form_instance})



@method_decorator(signin_required,name="dispatch")
class TransactionDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Transactions.objects.get(id=id).delete()

        return redirect('transaction-add')

@method_decorator(signin_required,name="dispatch")
class ExpenceSummaryView(View):

    def get(self,request,*args,**kwargs):

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        qs=Transactions.objects.filter(created_date__month=cur_month,
                                       created_date__year=cur_year,
                                       owner=request.user,
                                       )
        
        total_expence=qs.values("amount").aggregate(total=Sum("amount"))

        # print(total_expence)

        category_summary=qs.values("category_object__name").annotate(total=Sum("amount"))
        
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))

        data={
            "total_expence":total_expence.get("total"),
            "category_summary":category_summary,
            "payment_summary":payment_summary

        }


        return render(request,"expence_summary.html",data)
    
@method_decorator(signin_required,name="dispatch")
class TransactionSummaryView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionFilterForm

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        if 'start_date' in request.GET and 'end_date' in request.GET:

            start_date=request.GET.get("start_date")
            end_date=request.GET.get("end_date")
            qs=Transactions.objects.filter(
                created_date__range=(start_date,end_date)
            )
        else:
            qs=Transactions.objects.filter(
                created_date__month=cur_month,
                created_date__year=cur_year
            )

        return render(request,"transaction_summary.html",{"transactions":qs,"form":form_instance})
    
#  looksups
# >(__gt)
# <(__lt)


class ChartView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'chart.html')
        


class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"signup successfully")

            print("account created successfully")

            return redirect("signin")
        else:
            messages.error(request," signup failed")
            # print("failed to create account")

            return render(request,"register.html",{"form":form_instance})


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):


        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

        
            

            user_obj=authenticate(request,**form_instance.cleaned_data)

            if user_obj:

                login(request,user_obj)
                messages.error(request," signin successfull")
                return redirect("summary")
            messages.error(request," signin failed")
          
        
        return render(request,"login.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")



                                        

