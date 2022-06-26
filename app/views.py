from django import views
from django.shortcuts import render
from . models import Product
from .forms import CustomerRegistrationForm ,LoginForm , CustomerProfileForm
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .models import User ,  Customer


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




def orders(request):
 return render(request, 'app/orders.html')

def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
	def get(self, request):
		# totalitem = 0
		# if request.user.is_authenticated:
		# 	totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})
		# return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		# totalitem = 0
		# if request.user.is_authenticated:
		# 	totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
      
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary',})
		# return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})




def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{"add":add,"active":"btn-primary"})










# navbar page making@ 2:15:00 topwear bottomwear
def mobile(request):
  return render(request, 'app/mobile.html')


