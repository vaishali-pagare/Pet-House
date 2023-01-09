from django.shortcuts import render,redirect
from AdminApp.models import Category,Pets,UserInfo,Pet_Cat,PaymentMaster,Appointment,Old_Order
from django.http import HttpResponse
from django.contrib import messages
from UserApp.models import MyCart
from twilio.rest import Client
import random
from django.contrib import messages

# Create your views here.

def homepage(request):
    cat = Category.objects.all()
    pet = Pets.objects.all()
    return render(request,'homepage.html',{'category':cat,'pet':pet})


def login(request):
    uname = request.POST["username"]
    pwd = request.POST["password"]
    pet = Pets.objects.all()
    
    try:
        user = UserInfo.objects.get(username=uname, pwd=pwd)
    except:
        alert = "!!.Invalid Credential..!!"
        return render(request,"homepage.html",{"alert1":alert,'pet':pet})

    else:
        request.session["uname"] = user.username
        if ("uname" in request.session):
            request.session["fname"] = user.fname
            return redirect(homepage)
        

def about(request):
    cat = Category.objects.all()
    return render(request,"about.html",{"category":cat})

def gallary(request):
    cat = Category.objects.all()
    pet = Pets.objects.all()
    return render(request,"gallary.html",{"category":cat,"pet":pet})

def contact(request):
    cat = Category.objects.all()
    return render(request,"contact.html",{"category":cat})

def signup(request):
    pet = Pets.objects.all()
    fname = request.POST["fname"].upper()
    lname = request.POST["lname"].upper()
    mob = request.POST["mob"]
    username = request.POST["user"]
    password = request.POST["pwd"]
    user = UserInfo()
    user.fname = fname
    user.lname = lname
    user.mobile = mob
    user.username = username
    user.pwd = password
    try:
        user.save()
    except:
        alert = "!!.USER-NAME EXIST.!!"
        return render(request,"homepage.html",{"alert1":alert,'pet':pet})
        
    else:
        alert = "!!.SIGN-UP SUCCESSFULL.!!"
        return render(request,"homepage.html",{"alert1":alert,'pet':pet})
        

def logout(request):
    request.session.clear()
    return redirect(homepage)

def viewsSection(request,id):
    animl = Pet_Cat.objects.filter(pet=id)
    cat = Category.objects.all()
    pet = Pets.objects.all()
    return render(request, "viewsSection.html",{'category':cat,'pet':pet,'animl':animl})

def showPets(request,id):
    pets = Pets.objects.filter(cat=id)
    cat = Category.objects.all()
    return render (request,"gallary.html",{'category':cat,'pet':pets})

def readMore(request,id):
    cat = Category.objects.all()
    try:
        animl = Pet_Cat.objects.get(id=id)
    except:
        return redirect(homepage)

    else:
        return render (request,"readMore.html",{'category':cat,'animl':animl})

def addTocart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            petid = request.POST['petid']
            user = request.session['uname']
            pet = Pet_Cat.objects.get(id=petid)
            user = UserInfo.objects.get(username = user)

            try:
                cart = MyCart.objects.get(pet=pet, user=user)
                            
            except:
                cart = MyCart()
                cart.user = user
                cart.pet=pet
                cart.save()
                return redirect(showAllCart)

            else:
                messages.success(request, "* Already In Cart")
                return redirect(showAllCart)
        
        else:
            pet = Pets.objects.all()
            alert = "!!..PLEASE SIGN-IN..!!"
            return render(request,"homepage.html",{"alert1":alert,'pet':pet})

def showAllCart(request):
    cat = Category.objects.all()
    if(request.method =="GET"):
        uname = request.session["uname"]
        user = UserInfo.objects.get(username = uname)
        cartitem = MyCart.objects.filter(user=user)
        his = Old_Order.objects.filter(user=user.id)
        #print(cartitem.id)
        total = 0
        for item in cartitem:
            total = (total) + float(item.pet.price)

        request.session["total"] = total
        return render(request,"showAllCart.html",{'item':cartitem,'category':cat,'history':his})

    
def removeItem(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(username = uname)
    id = request.POST["petid"]
    pet = Pet_Cat.objects.get(id=id)
    item = MyCart.objects.get(user=user,pet=pet)
    item.delete()
    return redirect(showAllCart)

def MakePayment(request):
    cat = Category.objects.all()
    if(request.method == "GET"):
        return render(request, "makepayment.html",{'category':cat})

    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]

        try:
            buyer = PaymentMaster.objects.get(cardno = cardno,cvv=cvv,expiry=expiry)

        except:
            alert = "* INVALID-DETAILS"
            return render(request,"makepayment.html",{"alert":alert})

        else:
        

            try:                       
                genotp = random.randint(10000, 99999)

                account_sid = "ACbbe2bf533eb6d2a5e470361ca725aefd"
                auth_token = "b711e85df2f2491b7c2cb54cfacb748c"

                client = Client(account_sid, auth_token)

                msg = client.messages.create(
                    body = f"Hello...!!! PET-HOUSE Sending OTP:{genotp}", # alwayz connectt net
                    from_ ="+16506403455",
                    to = "+91"+str(buyer.mobile)
                )
                msgs="* OTP send to your mobile Number"
                return render(request, "otp.html",{'buyer':buyer, 'cardno':cardno, 'cvv':cvv,'expiry':expiry, 'genotp':genotp,'msg':msgs})
            
            except:
                msgs="* Please Connect to Internet"
                return render(request, "otp.html",{'buyer':buyer, 'cardno':cardno, 'cvv':cvv,'expiry':expiry, 'genotp':genotp,'msgs':msgs})
               
                        
                        #data=genotp
                        
                        #return render_template("signUp.html",msgs=msgs,nm=nm, accNum=accNum, mobile=mobile,genotp=genotp)
               

def otp(request):
    
    if(request.method == "POST"):
        finum = request.POST["num1"]
        snum = request.POST["num2"]
        tnum = request.POST["num3"]
        fonum = request.POST["num4"]
        fivnum = request.POST["num5"]
        otpp = request.POST["otpp"]
        cardno = request.POST["cardno"]
        cvv =  request.POST["cvv"]
        expiry =  request.POST["expiry"]

        num = finum+snum+tnum+fonum+fivnum
  
        if(int(otpp) == int(num)):
            

            try:
                buyer = PaymentMaster.objects.get(cardno = cardno,cvv=cvv,expiry=expiry)

            except:
                alert = "* INVALID-DETAILS"
                return render(request,"makepayment.html",{"alert":alert})

            else:
                owner = PaymentMaster.objects.get(cardno="00000",cvv="000",expiry="23/2030")
                
                if(int(buyer.balance) > 0 and int(buyer.balance)>=int(request.session["total"]) ):
                    owner.balance = float(owner.balance) + float(request.session["total"])
                    buyer.balance = float(buyer.balance) - float(request.session["total"])
                    buyer.save()
                    owner.save()
                    uname = request.session["uname"]
                    user = UserInfo.objects.get(username=uname)
                    order = Old_Order()
                    order.user = user
                    order.amount = request.session["total"]
                    details = " "
                    items = MyCart.objects.filter(user=user)
                    for item in items:
                        details += (item.pet.category)+ " ,"
                        item.delete()
                    order.details = details
                    order.save()
                    tot = request.session["total"]
                    account_sid = "ACbbe2bf533eb6d2a5e470361ca725aefd"
                    auth_token = "b711e85df2f2491b7c2cb54cfacb748c"

                    client = Client(account_sid, auth_token)

                    msg = client.messages.create(
                        body = f"Payment Received: {tot} rupees, from: {buyer.mobile}" ,
                        from_ ="+16506403455",
                        to = "+91"+str(owner.mobile)
                    )
                    msg= "* !!..PAYMENT SUCCESSFULL..!!"
                    return render(request,"license.html",{"msgs":msg})
                
                else:
                   
                    alert = "* INSUFFICIENT-FUND"
                    return render(request,"makepayment.html",{"alert":alert})

        else:
            buyer = PaymentMaster.objects.get(cardno = cardno,cvv=cvv,expiry=expiry)
            msg="* OOPS...!! OTP Not Match"
            return render (request, "otp.html",{"msgs":msg,"genotp":otpp,"cardno":cardno,"cvv":cvv,"expiry":expiry,"buyer":buyer})
              
def license(request):
    if(request.method =="POST"):
        fname = request.POST["fname"]
        mob = request.POST["mob"]
        addr = request.POST["addr"]
        date = request.POST["date"]
        slot = request.POST["slot"]                                                 
        location = request.POST["location"]

        if(slot == "1"):
            time="9:00-10:00 AM"
        elif(slot == "2"):
            time="11:00-12:00 PM"
        elif(slot == "3"):
            time="1:00-2:00 PM"
        elif(slot == "4"):
            time="3:00-4:00 PM"
        elif(slot == "5"):
            time="4:30-6:30 PM"

        if(location == "1"):
            loc="Pune"                            
        elif(location == "2"):
            loc="Aurangabad"
        elif(location == "3"):
            loc="Mumbai"
        elif(location == "4"):
            loc="Chennai"

        apoint = Appointment()
        apoint.name = fname
        apoint.mobile =mob
        apoint.address = addr
        apoint.date = date
        apoint.slottime = time
        apoint.location = loc
        apoint.save()
        account_sid = "ACbbe2bf533eb6d2a5e470361ca725aefd"
        auth_token = "b711e85df2f2491b7c2cb54cfacb748c"

        client = Client(account_sid, auth_token)

        msg = client.messages.create(
            body = f"Hurry...!!! Your Appointment for Pet_License is booked at: {apoint.date} time: {apoint.slottime} location: {apoint.location}." ,
            from_ ="+16506403455",
            to = "+91"+str(apoint.mobile)
        )
        return render (request,"confirm.html",{})





    




    


