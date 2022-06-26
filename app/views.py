from django.shortcuts import render
from . models import Product
from .forms import CustomerRegistrationForm ,LoginForm
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .models import User


#Landing page 

def home(request):
 topwear = Product.objects.filter(category="TW")
 mobile = Product.objects.filter(category="M")
 bottomwear = Product.objects.filter(category="BW")
 return render(request, 'app/home.html',{"topwear":topwear,"mobile":mobile,"bottomwear":bottomwear})

#EndLanding page


# Productdetailpage
def product_detail(request,id):
    product = Product.objects.get(pk=id)
    return render(request, 'app/productdetail.html',{"product":product})

#endProductdetailpage

# userregistration
class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
  
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
   return HttpResponseRedirect("/registration/")
  
  return render(request, 'app/customerregistration.html', {'form':form})
  

# enduser registration



def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')





# def checkout(request):
#  return render(request, 'app/checkout.html')




# navbar page making@ 2:15:00 topwear bottomwear
def mobile(request):
  return render(request, 'app/mobile.html')


