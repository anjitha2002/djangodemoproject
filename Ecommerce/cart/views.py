from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart
import razorpay
from cart.models import Payment,Order_details


# Create your views here.
def addtocart(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        c.quantity+=1
        p.stock-=1
        p.save()
        c.save()
    except:
        c=Cart.objects.create(user=u,product=p,quantity=1)
        p.stock -= 1
        p.save()
        c.save()

    return redirect('cart:cartview')

def cartview(request):
    u=request.user
    c=Cart.objects.filter(user=u) #to filter cart record for a particular user
    #to calculate total value
    total=0
    for i in c:
        total+=i.quantity*i.product.price


    context={'cart':c,'total':total}
    return render(request, 'cart.html',context)


def cartremove(request,i):
    u=request.user
    p=Product.objects.get(id=i)
    try:
        c=Cart.objects.get(user=u,product=p)
        if(c.quantity > 1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock+=1
            p.save()
    except:
        pass
    return redirect('cart:cartview')

def carttrash(request,i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)
        c.delete()
        p.stock+=c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')


def placeorder(request):
    if request.method=='POST':
        a=request.POST['A']
        ph= request.POST['P']
        pi = request.POST['Pi']

        # for cal total billing amount
        u=request.user
        c = Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        # print(total)

        # razorpay client connection
        client=razorpay.Client(auth=('rzp_test_x6U04M5PAqZ8UM','ky27RY2LyHfZ8hmN8f1VE0ib'))
        # Razorpay order creation
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']#retrieve the order id from response
        status=response_payment['status']#retrieve the status from response
        if(status=="created"):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()

            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,phone=ph,address=a,pin=pi,order_id=order_id,no_of_items=i.quantity)
                o.save()

            context={'payment':response_payment,'name':u.username}

            return render(request, 'payment.html',context)

    return render(request,'placeorder.html')

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login

@csrf_exempt
def payment_status(request,p):
    user=User.objects.get(username=p)
    login(request,user)
    response=request.POST
    print(response)

    #check the validity of payment details received from razorpay
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    client = razorpay.Client(auth=('rzp_test_x6U04M5PAqZ8UM', 'ky27RY2LyHfZ8hmN8f1VE0ib'))
    try:
        status=client.utility.verify_payment_signature(param_dict)  #for checking the payment details   #we pass param_dict to verify payment_signature fn
        print(status)
        p=Payment.objects.get(order_id=response['razorpay_order_id'])  #after successfull payment retreive the payment record matching with response['order_id']
        p.razorpay_payment_id=response['razorpay_payment_id']  #assign response [payment_id] to razorpay_payment_id
        p.paid=True  #assign paid value to true
        p.save()

        o=Order_details.objects.filter(order_id=response['razorpay_order_id'])# aftersuccessfulll paymet retrieve the order_details records matching with response
        for i in o:
            i.payment_status="completed"  #assign "completed" to payment_status in each record\
            i.save()
            #to remove cart items fr a particular user after successfull payment
            c=Cart.objects.filter(user=user)
            c.delete()



    except:
        pass




    return render(request,'payment_status.html')

def order_view(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status="completed")
    context={'orders':o}

    return render(request,'orderview.html',context)




