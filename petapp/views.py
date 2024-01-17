from django.shortcuts import render,redirect
from django.template import loader
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import pet,user,cart,order,orderdetail
from .forms import petform,Userform
from django.views.generic import ListView,DetailView,CreateView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from datetime import date

def menu(request):
    template=loader.get_template('menubar.html')
    return HttpResponse(template.render())
class PetList(ListView):
    model=pet
    template_name='petlist.html'
    context_object_name='petobj'
    def get_context_data(self,**kwargs):
        data=self.request.session['username']
        context=super().get_context_data(**kwargs)
        context['session']=data
        return context

class PetDetail(DetailView):
    model=pet   
    template_name='petdetail.html'
    context_object_name='petdetail' 

class petlistviewCM(ListView):
    queryset=pet.pets.get_pet_age()
    template_name='petlist.html'
    context_object_name='petobj'

def nav(request):
    return render(request,'menubar.html',{'session':request.session['username']})

def search(request):
    if request.method=='POST':
        sq=request.POST.get('searchquery')
        result=pet.pets.filter(Q(Breed__icontains=sq)|Q(Species__icontains=sq)|Q(Name__icontains=sq)|Q(Gender__iexact=sq))
        return render(request,'petlist.html',{'petobj':result}) 


def registration(request):
    if request.method=='GET':
        return render(request,'registration.html')
    elif request.method=='POST':
        fn=request.POST.get('firstname')
        ln=request.POST.get('lastname')
        Email=request.POST.get('youremail')
        Password=request.POST.get('yourpassword')
        passw=make_password(Password)
        cpassword=request.POST.get('confirmpassword')
        phoneno=request.POST.get('phone')
        Address=request.POST.get('Address')
        City=request.POST.get('yourcity')
        State=request.POST.get('yourstate')
        Pin=request.POST.get('statepin')

        userobj=user(firstname=fn,lastname=ln,email=Email,password=passw,confirmpassword=cpassword,contact=phoneno,address=Address,city=City,state=State,pincode=Pin)
        userobj.save()
        return redirect ('Login')
        # return HttpResponse('User registered successfully')

def login(request):
    if request.method=='GET' :
        return render(request,'login.html')
    elif request.method=='POST':
        User=user.objects.filter(email=request.POST.get('email'))
        if User:
            userobj=user.objects.get(email=request.POST.get('email'))
            passfe=request.POST.get('pass')
            flag=check_password(passfe,userobj.password)
            if flag:
                request.session['username']=request.POST.get('email')
                session=request.session['username']
                return redirect('../petlist/')
                # return render(request,'petlist.html',{'session':session})
            else:
                return HttpResponse('Wrong username or Password')    
        # return redirect('petList')
        # you can also write return render code insteadof redirect 
        # return render(request,'login.html')  
def addtocart(request):
    productid=request.POST['pid']
    pobj=pet.pets.get(id=productid)
    usersession = request.session['username']
    cobj = user.objects.get(email =usersession)
    flag=cart.objects.filter(customerid_id=cobj.id,productid_id=pobj)
    if flag:
        cartobj=cart.objects.filter(customerid_id=cobj.id,productid_id=pobj)
        print(cartobj)
        cartobj.quantity=cartobj.quantity + 1;
        cartobj.Totalamt=cartobj.quantity * pobj.Price;
        cartobj.save()
    else:
        cartobj=cart(quantity=1,Totalamt=pobj.Price,customerid_id=cobj.id,productid_id=pobj)
        cartobj.save()
    cartobjdisplay=cart.objects.filter(customerid_id=cobj.id)
    return  render(request,'petlist.html',{'session':usersession,'petobj':pet.pets.all()})
    
    # usersession='sr@gmail.com'
    # print(request.session['username'])
      
def viewcart(request):
    usersession=request.session['username']
    userobj=user.objects.get(email=usersession)
    cartobj=cart.objects.filter(customerid_id=userobj.id)
    return render(request,'cart.html',{'petobj':cartobj,'session':usersession})

def changequantity(request):
    usersession=request.session['username']
    userobj=user.objects.get(email=usersession)
    pid=request.POST.get('pid')
    
    bq=request.POST['buttonquantity']
    if bq=='+':
        cartobj=cart.objects.get(customerid_id=userobj.id,productid_id=pid)
        cartobj.quantity=cartobj.quantity+1
        cartobj.Totalamt=cartobj.quantity * cartobj.productid.Price
        cartobj.save()
    else:
        cartobj=cart.objects.get(customerid_id=userobj.id,productid_id=pid)
        
        cartobj.quantity=cartobj.quantity-1
        quan=cartobj.quantity   
        cartobj.Totalamt=cartobj.quantity * cartobj.productid.Price
        if quan==0:
            cartobj.delete()
        else:
              cartobj.save()
    cartobj=cart.objects.filter(customerid_id=userobj.id)
    return render(request,'cart.html',{'petobj':cartobj,'session':usersession})

def summarypage(request):
    usersession=request.session['username']
    userobj=user.objects.get(email=usersession)
    cartobj=cart.objects.filter(customerid_id=userobj.id)
    totalbill=0
    # totalquantity=0
    for i in cartobj:
        # totalqauntity=i.quantity+totalquantity
        totalbill=i.Totalamt+totalbill
    return render(request,'summary.html',{'session':usersession,'petobj':cartobj,'totalbill':totalbill})

def payment(request):
    return render(request,'payment_page.html')

def placeorder(request):
    usersession=request.session['username']
    userobj=user.objects.get(email=usersession)
    nam=request.POST.get('name')
    addres=request.POST.get('address')
    phonen=int(request.POST.get('phoneno'))
    cit=request.POST.get('city')
    stat=request.POST.get('state')
    pincod=int(request.POST.get('pincode'))
    totalbillamoun=float(request.POST.get('totalbillamount'))
    orderobj=order(firstname= nam,city = cit,state=stat,address = addres, contact = phonen,pincode = pincod,totalbillamount = totalbillamoun)
    orderobj.save()
    dateobj = date.today()

    print(dateobj)
    datedata = str(dateobj).replace('-','')

    orderno = str(orderobj.id) + datedata
    orderobj.ordernumber = orderno
    orderobj.save()

    cartobj = cart.objects.filter(customerid = userobj.id)

    for i in cartobj:
        orderdetailobj = orderdetail(ordernumber = orderno, productid = i.productid,customerid = i.customerid,quantity = i.quantity,totalprice = i.Totalamt)
        orderdetailobj.save()
        i.delete()

    orderdetailobjdisplay=orderdetail
    return render(request,'payment_page.html',{'orderobj':orderobj})
    
def logout(request):
    request.session['username']=''
    return redirect('login.html')    