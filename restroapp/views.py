from django.shortcuts  import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from restroapp.models import Product,Cart,Order
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

# Create your views here.
def index(request):
    p=Product.objects.filter(is_active=True)
   
    context={}
    context['data']=p
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def menu(request):
    return render(request,'menu.html')

def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']

       
        u=authenticate(username=n,password=p)
        context={} 
        if u==None:
            context['ermsg']="Invalid credentails!"
            return render(request,'login.html',context)
        else:
            login(request,u)
            return redirect('/index')
        
def user_logout(request):
    logout(request)
    return redirect('/index')

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        n=request.POST['uname']
        e=request.POST['email']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        
        context={}
        if n=="" or e=="" or p=="" or cp=="":
            context['ermsg']="Plaease fill out all Fileds"
        elif p!=cp:
            context['ermsg']="Password and confirm password must be same!"
        elif len(p)<8:
            context['ermsg']="Password should be equal to 8 char"
        else:
            u=User.objects.create(username=n,email=e)
            u.set_password(p)
            u.save()
            context['success']="Registered Successfully...!"
        
        return render(request,'signup.html',context)
    
# Filter 

def catfilter(request,cid):
    q1=Q(cat=cid)             #show pr of catogory eith id
    q2=Q(is_active=True)     #show active products only
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def sort(request,sid):
    context={}
    if sid==1:
        p=Product.objects.order_by('price').filter(is_active=True)
    else:
        p=Product.objects.order_by('price').filter(is_active=True)

    context['data']=p 
    
    return render(request,'index.html',context)

def pricefilter(request):
   
   
    min=request.GET['min']
    max=request.GET['max']
    context={} 

    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Product.objects.filter(q1 & q2).filter(is_active=True)
    context['data']=p

    return render(request,'index.html',context)



def search(request):
    search=request.GET['search']
    # n=Product.objects.filter(name__icontains=search) ----for single column

    n=Product.objects.filter(name__icontains=search)
    pdet=Product.objects.filter(pdetail__icontains=search)
    context={}
    all=n.union(pdet)

    if len(all)==0:
        context['ermsg']="Products Not Found..!!"
    
    context['data']=all

    return render(request,'index.html',context)

def products(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'products.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)

        # print("User Looged in..")
        # u=request.user.id
       
    
        context={}
        context['data']=p
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        if len(c)==0:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']='Product Added Successfully..!!'
            return render(request,'products.html',context)
        else:
            context['ermsg']='Product Already Added in Cart..!!'
            return render(request,'products.html',context)    
    else:

        return redirect('/login')
    
def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    context={}
    context['data']=c
    s=0
    for i in c:
        s=s+i.pid.price*i.qty
    context['total']=s
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty  
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1

    c.update(qty=q)
    return redirect('/cart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def place_order(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        amt=i.qty*i.pid.price
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=amt)
        o.save()
        i.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt
    context={'data':o,'total':s,'n':len(o)}

    return render(request,'place_order.html',context)
def remove(request,cid):
    o=Order.objects.filter(id=cid)
    o.delete()
    return redirect('/place_order')

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_HeYv5uvRUwSNEa", "FKsfWPzm770aRcJaLCP1tSOh"))
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt

    data = { "amount": s * 100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    context={'payment':payment}
    # print(payment)
    return render(request,'pay.html',context)

def success(request):
    sub="Order Status"
    msg="Order Placed Successfully...!!"
    frm='ujjawala992001@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )                               
    return render(request,'success.html')

