from django.shortcuts import render,redirect
from.models import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models.aggregates import Sum
from django.core.mail import send_mail


# Create your views here.

def index(request):
    return render(request,"index.html")

def addfish(request):
    return render(request,"addfishes.html")

def savefishdata(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        description = request.POST.get('desc')
        image = request.FILES['image']
        data= addfishcategory(name=name,description=description,image=image)
        data.save()
        return redirect('addfish')


def showdetails(request):
    data = addfishcategory.objects.all()
    return render(request,"showdetail.html",{'data':data})


def editbyid(request,eid):
    data = addfishcategory.objects.filter(id=eid)
    return render(request,"editfishcat.html",{'data':data})

def updatefishdata(request,uid):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('desc')
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
        except MultiValueDictKeyError:
            file = addfishcategory.objects.get(id=uid).image

        data = addfishcategory.objects.filter(id=uid).update(name=name, description=description,image=file)
    return redirect("showdetails")



def deletebyid(request,did):
    data = addfishcategory.objects.filter(id=did)
    data.delete()
    return redirect("showdetails")


def products(request):
    data = addfishcategory.objects.all()
    return render(request, "product.html", {'data': data})

def savefishdetals(request):
    if request.method == 'POST':
        fishcategory= request.POST.get('fishcategory')
        proname = request.POST.get('proname')
        proprice = request.POST.get('proprice')
        proqty = request.POST.get('proqty')
        image = request.FILES['image']
        data= addfishdetatls(fishcategory=fishcategory,proname=proname,proprice=proprice,proqty=proqty,image=image)
        data.save()
        return redirect('products')

def showproduct(request):
    data = addfishdetatls.objects.all()
    return render(request, "showproduct.html", {'data': data})

def editproductbyid(request,eid):
    category = addfishcategory.objects.all()
    data = addfishdetatls.objects.filter(id=eid)
    return render(request,"editproduct.html",{'data':data,'category':category})

def updateproductfishdata(request,uid):
    if request.method == 'POST':
        fishcategory = request.POST.get('fishcategory')
        proname = request.POST.get('proname')
        proprice = request.POST.get('proprice')
        proqty = request.POST.get('proqty')
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
        except MultiValueDictKeyError:
            file = addfishdetatls.objects.get(id=uid).image

        data = addfishdetatls.objects.filter(id=uid).update(fishcategory=fishcategory, proname=proname,proprice=proprice,proqty=proqty,image=file)
    return redirect("showproduct")


def deleteproductbyid(request,did):
    data = addfishdetatls.objects.filter(id=did)
    data.delete()
    return redirect("showproduct")



def showorders(request):
    data = checkoutdet.objects.all()
    return render(request, "showorder.html", {'data': data})

def home(request):
    data = addfishcategory.objects.all()
    return render(request, "user/index.html", {'data': data})


def accountregistration(request):
    return render(request,"user/registration.html")

def saveuserregistration(request):
    if request.method == 'POST':
        fname= request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        data= saveuser(fname=fname,lname=lname,email=email,password=password)
        data.save()
        c = "Your Username :- " + email + " Your Password :- " + password
        send_mail(
            'Fresh Fish',
            'Welcome To Our Freshfish Cart' + " " + c,
            'freshfishcart1234@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('accountlogin')

def accountlogin(request):
    return render(request, "user/login.html")

def getlogindata(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if(email=='admin@gmail.com' and password=="test123"):
        return render(request,'index.html')
    elif saveuser.objects.filter(email=email, password=password).exists():
        data = saveuser.objects.filter(email=email, password=password).values('fname', 'lname',
                                                                        'id').first()
        request.session['fname'] = data['fname']
        request.session['lname'] = data['lname']
        request.session['email'] = email
        request.session['password'] = password
        request.session['id']=data['id']

        return redirect('home')
    else:
        return render(request, 'user/login.html', {'msg': "Sorry Invalid username or password"})

def logout(request):
    del request.session['email']
    del request.session['fname']
    del request.session['lname']
    del request.session['password']
    del request.session['id']
    return redirect('home')


def productall(request,category):
    if category == "all":
        data= addfishdetatls.objects.all()
    else:
        data= addfishdetatls.objects.filter(fishcategory=category)
    return render(request,"user/productall.html",{'data':data})

def fishdetails(request,fid):
    data = addfishdetatls.objects.filter(id=fid)
    return render(request,"user/fishdetail.html",{'data':data})

def fishdet(request):
    return render(request,"user/fishdetail.html")

def cart(request):
    u = request.session.get('id')
    data = Fwcart.objects.filter(userid=u,status=0)
    return render(request,"user/cart.html",{'data':data})

def fish_cart(request,sid):
    if 'id' in request.session:
        total = request.POST.get('total')
        quantity = request.POST.get('quan')
        userid = request.POST.get('id')
        data = Fwcart(productid=addfishdetatls.objects.get(id=sid), quantity=quantity, total=total,
                       userid=saveuser.objects.get(id=userid), status=0)
        data.save()
        return redirect('cart')

@csrf_exempt
def cart_update(request):
    if request.method == "POST":
        cartid = request.POST.get('pid')
        q = request.POST.get('qty')
        print(q)
        p = request.POST.get('price')
        tot = float(q)*float(p)
        print(tot)
        Fwcart.objects.filter(id=cartid).update(total=tot,quantity=q)
    return HttpResponse()

def cartdeletedata(request,cdid):
    data = Fwcart.objects.filter(id=cdid)
    data.delete()
    return redirect('cart')

def checkoutdetails(request):
    u = request.session.get('id')
    data = Fwcart.objects.filter(userid=u ,status=0)
    count = Fwcart.objects.filter(userid=u,status=0).count()
    total = Fwcart.objects.filter(userid=u,status=0).aggregate(Sum('total'))

    return render(request, "user/checkout.html",{'data':data,'count':count,'total':total})

def contact(request):
    return render(request,"user/contactus.html")

def aboutus(request):
    return render(request,"user/aboutus.html")

def contactdata(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        sub = request.POST.get('sub')
        msg = request.POST.get('message')
        data = savecontactdata(fname=fname,email=email,sub=sub,msg=msg)
        data.save()
        return redirect('contact')

def shippingaddr(request):
    if request.method == 'POST':
        finame = request.POST.get('finame')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        shippingmethod = request.POST.get('shippingmethod')
        u= request.session.get('id')
        order = Fwcart.objects.filter(userid=u,status=0)
        for i in order:
           data = checkoutdet(cartid=Fwcart.objects.get(id=i.id),finame=finame,lname=lname,uname=uname, email=email, add1=add1,add2=add2,country=country,state=state,zip=zip,shippingmethod=shippingmethod)
           data.save()
           Fwcart.objects.filter(id=i.id).update(status=1)
    return redirect('home')



