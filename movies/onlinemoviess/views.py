from django.shortcuts import render,redirect
from onlinemoviess.models import Movie
# Create your views here.
def home(request):
    k = Movie.objects.all()
    context = {'movie': k}
    return render(request,"home.html",context)
def addmovies(request):
    if(request.method=="POST"):
        t=request.POST['T']
        d=request.POST['D']
        l = request.POST['L']
        y = request.POST['Y']
        i = request.FILES['I']
        m=Movie.objects.create(title=t,description=d,language=l,year=y,image=i)
        m.save()
        return redirect('home')


    return render(request,"addmovies.html")
def detail(request,p):
    m=Movie.objects.get(id=p)
    context={'movie':m}
    return render(request,"detail.html",context)
def delete(request,p):
    d=Movie.objects.get(id=p)
    d.delete()
    return redirect('home')
def update(request,p):
    u=Movie.objects.get(id=p)
    if (request.method == "POST"):
        u.title = request.POST['T']
        u.description = request.POST['D']
        u.language = request.POST['L']
        u.year= request.POST['Y']
        if(request.FILES.get('I')==None):
            u.save()
        else:
            u.image=request.FILES.get('I')
        return redirect('home')
    context={'movie':u}
    return render(request, "update.html", context)