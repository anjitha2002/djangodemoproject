from django.shortcuts import render,redirect
from shop.models import Category,Product

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout



# Create your views here.
def catagory(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'categories.html',context)

@login_required()
def product(request,i):
    c=Category.objects.get(id=i)
    p=Product.objects.filter(category=c)
    context={'cat':c,'pro':p}
    return render(request,'product.html',context)

@login_required()
def product_details(request,i):
    p = Product.objects.get(id=i)
    context={'pro':p}
    return render(request,'detail.html',context)


def register(request):
    if(request.method=="POST"):
        U=request.POST['U']
        P=request.POST['P']
        C=request.POST['C']
        E=request.POST['E']
        F=request.POST['F']
        L=request.POST['L']
        if (P==C):
            u=User.objects.create_user(username=U,password=P,email=E,first_name=F,last_name=L)
            u.save()
        else:
            return HttpResponse("Password should be same")
        return redirect('shop:catagory')

    return render(request,'register.html')


def user_login(request):
    if (request.method == "POST"):
        U = request.POST['U']
        P = request.POST['P']
        shop = authenticate(username=U, password=P)
        if shop:
            login(request, shop)
            return redirect('shop:catagory')
        else:
            return HttpResponse("invalid credentials")

    return render(request, 'login.html')




def user_logout(request):
    logout(request)
    return redirect('shop:login')

def add_category(request):
    if (request.method == "POST"):
        N= request.POST['N']
        I = request.FILES['I']
        D = request.POST['D']


        c = Category.objects.create(name=N,image=I,desc=D)
        c.save()

        return redirect('shop:catagory')

    return render(request,'add_category.html')

def add_product(request):

    if (request.method == "POST"):
        N = request.POST['N']
        I = request.FILES['I']
        D= request.POST['D']
        P = request.POST['P']
        S = request.POST['S']
        # A = request.POST['A']
        C=request.POST['C']
        cat = Category.objects.get(name=C)


        p = Product.objects.create(name=N,image=I,desc=D,price=P,stock=S,category=cat)
        p.save()

        return redirect('shop:catagory')

    return render(request,'add_product.html')


def addstock(request,i):
    p=Product.objects.get(id=i)
    if(request.method=='POST'):
        p.stock = request.POST['S']
        p.save()
        return redirect('shop:detail',i)

    context={'pro':p}

    return render(request,'addstock.html',context)

















