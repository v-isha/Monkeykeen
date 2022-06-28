from django import dispatch, views
from django.shortcuts import render , redirect ,HttpResponse
from . models import Product
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
# from django.contrib.auth import authenticate,login,logout
from .models import Customer , Cart ,OrderPlaced
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#Landing page 

def home(request):
 totalitem =0
 topwear = Product.objects.filter(category="TW")
 mobile = Product.objects.filter(category="M")
 bottomwear = Product.objects.filter(category="BW")
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 
 return render(request, 'app/home.html',{"topwear":topwear,"mobile":mobile,"bottomwear":bottomwear,"totalitem":totalitem})

#EndLanding page


# Productdetailpage
def product_detail(request,id):
	totalitem =0
	item_already_in_cart=False
	product = Product.objects.get(pk=id)
	if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
	
	return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

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

# cart
@login_required()
def add_to_cart(request):
	user = request.user
	product = request.GET.get('prod_id')
	product_title = Product.objects.get(id=product)
	Cart(user=user, product=product_title).save()
	messages.success(request, 'Product Added to Cart Successfully !!' )
	return redirect('/cart')

@login_required()
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 70.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
		else:
			return render(request, 'app/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'app/emptycart.html', {'totalitem':totalitem})





@login_required()
def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")
@login_required()
def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required()
def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")
@login_required()
def checkout(request):
	totalitem =0
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount,"totalitem":totalitem})

@login_required()
def payment_done(request):
	custid = request.GET.get('custid')
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")



def orders(request):
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'app/orders.html', {'order_placed':op})
 
def buy_now(request):
 return render(request, 'app/buynow.html')


# end cart



@method_decorator(login_required(),name="dispatch")
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
			return redirect("address")
      
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary',})
		# return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
@login_required()
def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{"add":add,"active":"btn-primary"})



@login_required()
def mobile(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			mobiles = Product.objects.filter(category='M')
	elif data == 'mi' or data == 'Samsung':
			mobiles = Product.objects.filter(category='M').filter(brand=data)
	elif data == 'below':
			mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
	elif data == 'above':
			mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
	return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})



