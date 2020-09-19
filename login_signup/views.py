from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer, Vendor
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Vendor, Employee

def check_usertype(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user.id).exists():
            return 'customer'
        elif Vendor.objects.filter(user=request.user.id).exists():
            print('vendor')

# Create your views here.
def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('home_page'))
        else:
            # Handle Failed Login
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'auth/login.html')


def signup_view(request):
    check_usertype(request)
    if request.method == 'POST':

        user_type = request.POST.get('user_type')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_type.lower() == 'customer':
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            customer = Customer.objects.create(company_name=company_name, user=user)

        elif user_type.lower() == 'vendor':
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            vendor = Vendor.objects.create(company_name=company_name, user=user)

        return HttpResponseRedirect(reverse('home_page'))

    return render(request, 'auth/signup.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))