from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
# Create your views here.


def search(request):
    p=None  # initialize to None
    query=""

    if(request.method=="POST"):  # after form submission
        query=request.POST['q']
        if query:
            p=Product.objects.filter(Q(name__icontains=query )  |    Q(desc__icontains=query))      # icontains ---> lookups    (django lookup in w3schools)
           # datas to html
    context={'pro':p ,'query':query}
    return render(request,'search.html',context )
