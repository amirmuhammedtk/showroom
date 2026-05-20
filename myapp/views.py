from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,Group


# Create your views here.
from myapp.models import *


def login_get(request):
    return render(request,'login.html')

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']

    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request, user)
        if user.groups.filter(name='admin').exists():
            return redirect('/myapp/adminhome/')
        elif user.groups.filter(name='servicecenter').exists():
            return redirect('/myapp/servicecenterhome/')
        elif user.groups.filter(name='showroom').exists():
            showroom=Showroom.objects.get(USER=user)
            if showroom.status=='approved':
                return redirect('/myapp/showroomhome/')
            else:
                messages.warning(request,'you are not approved by admin')
                return redirect('/myapp/login_get/')
        elif user.groups.filter(name='user').exists():
            return redirect('/myapp/userhome/')
        else:
            messages.warning(request,'user not found')
            return redirect('/myapp/login_get/')
    else:
        messages.warning(request,'inavlid username or password')
        return redirect('/myapp/login_get/')


@login_required(login_url='/myapp/login_get/')
def adminhome(request):
    return render(request,'admin/adminhome.html')

@login_required(login_url='/myapp/login_get/')
def addcompany_get(request):
    return render(request,'admin/addcompany.html')
def addcompany_post(request):
    name=request.POST['name']
    description=request.POST['description']
    logo=request.FILES['logo']
    fs=FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fs.save(date, logo)
    path = fs.url(date)

    obj=Company()
    obj.name=name
    obj.description=description
    obj.logo=path
    obj.save()
    return redirect('/myapp/adminview_company/')

@login_required(login_url='/myapp/login_get/')
def adminview_company(request):
    a=Company.objects.all()
    return render(request,'admin/view_company.html',{'data':a})


@login_required(login_url='/myapp/login_get/')
def edit_company_get(request,id):
    data = Company.objects.get(id=id)
    return render(request,'admin/edit_company.html',{'data':data})


def edit_company_post(request):
    cid = request.POST['id']
    name = request.POST['name']
    description = request.POST['description']

    obj = Company.objects.get(id=cid)

    if 'logo' in request.FILES:
        logo = request.FILES['logo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, logo)
        path = fs.url(date)
        obj.logo = path
        obj.save()

    obj.name = name
    obj.description = description
    obj.save()
    return redirect('/myapp/adminview_company/')

def admindelete_company(request,id):
    obj = Company.objects.get(id=id)
    obj.delete()
    return redirect('/myapp/adminview_company/')


@login_required(login_url='/myapp/login_get/')
def add_vehiclemodel_get(request,id):
    company = Company.objects.get(id=id)
    return render(request,'admin/add_vehiclemodel.html',{'company':company})

def add_vehiclemodel_post(request):
    company_id = request.POST['company_id']
    model_name = request.POST['model_name']
    fuel_type = request.POST['fuel_type']

    obj = VehicleModel()
    obj.COMPANY = Company.objects.get(id=company_id)
    obj.model_name = model_name
    obj.fuel_type = fuel_type
    obj.save()

    return redirect('/myapp/adminview_vehiclemodel/')

@login_required(login_url='/myapp/login_get/')
def adminview_vehiclemodel(request):
    a=VehicleModel.objects.all()
    return render(request,'admin/viewvehiclemodel.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def edit_vehiclemodel_get(request,id):
    data = VehicleModel.objects.get(id=id)
    return render(request,'admin/edit_vehiclemodel.html',{'data':data})

def edit_vehiclemodel_post(request):
    vid = request.POST['id']
    model_name = request.POST['model_name']
    fuel_type = request.POST['fuel_type']

    obj = VehicleModel.objects.get(id=vid)
    obj.model_name = model_name
    obj.fuel_type = fuel_type
    obj.save()

    return redirect('/myapp/adminview_vehiclemodel/')

def admindelete_vehiclemodel(request,id):
    obj = VehicleModel.objects.get(id=id)
    obj.delete()
    return redirect('/myapp/adminview_vehiclemodel/')


@login_required(login_url='/myapp/login_get/')
def add_variant_get(request,id):
    model = VehicleModel.objects.get(id=id)
    return render(request,'admin/add_varient.html',{'model':model})


def add_variant_post(request):
    model_id = request.POST['model_id']
    variant_name = request.POST['variant_name']
    engine_cc = request.POST['engine_cc']
    mileage = request.POST['mileage']
    color = request.POST['color']
    photo = request.FILES['photo']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fs.save(date, photo)
    path = fs.url(date)

    obj = VehicleVariant()
    obj.MODEL = VehicleModel.objects.get(id=model_id)
    obj.variant_name = variant_name
    obj.engine_cc = engine_cc
    obj.mileage = mileage
    obj.color = color
    obj.photo = path
    obj.save()

    return redirect('/myapp/view_variant/')


@login_required(login_url='/myapp/login_get/')
def view_variant(request):
    data = VehicleVariant.objects.all()
    return render(request,'admin/view_varient.html',{'data':data})


@login_required(login_url='/myapp/login_get/')
def edit_variant_get(request,id):
    data = VehicleVariant.objects.get(id=id)
    return render(request,'admin/edit_varient.html',{'data':data})


def edit_variant_post(request):
    vid = request.POST['id']

    obj = VehicleVariant.objects.get(id=vid)
    obj.variant_name = request.POST['variant_name']
    obj.engine_cc = request.POST['engine_cc']
    obj.mileage = request.POST['mileage']
    obj.color = request.POST['color']

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        obj.photo = fs.url(date)

    obj.save()
    return redirect('/myapp/view_variant/')


def delete_variant(request,id):
    obj = VehicleVariant.objects.get(id=id)
    obj.delete()
    return redirect('/myapp/view_variant/')

@login_required(login_url='/myapp/login_get/')
def viewShowrooms(request):
    a=Showroom.objects.all()
    return render(request,'admin/viewshowroom.html',{'data':a})
def verifyshowroom(request,id):
    Showroom.objects.filter(id=id).update(status='approved')
    return redirect('/myapp/viewShowrooms/')
@login_required(login_url='/myapp/login_get/')
def viewapprovedshowrooms(request):
    a=Showroom.objects.filter(status='approved')
    return render(request,'admin/viewapprovedshowrooms.html',{'data':a})
@login_required(login_url='/myapp/login_get/')
def viewservicecenter(request):
    a=ServiceCenter.objects.all()
    return render(request,'admin/service center.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def viewusers(request):
    a=Customer.objects.all()
    return render(request,'admin/viewusers.html',{'data':a})
@login_required(login_url='/myapp/login_get/')
def viewfeedback(request):
    a=Feedback.objects.all()
    return render(request,'admin/viewfeedback.html',{'data':a})
@login_required(login_url='/myapp/login_get/')
def sendreply(request,id):
    a=Feedback.objects.get(id=id)
    return render(request,'admin/sendreply.html.html',{'data':a})
def sendreply_post(request):
    id=request.POST['id']
    reply=request.POST['reply']
    a=Feedback.objects.get(id=id)
    a.reply=reply
    a.status='replaid'
    a.save()
    return redirect('/myapp/viewfeedback/')

@login_required(login_url='/myapp/login_get/')
def admin_changePassword_get(request):
    return render(request,'admin/changepassword.html')
def admin_changePassword_post(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)
            return redirect('/myapp/login_get/')
        else:
            messages.warning(request, 'new password and confirm password must be same')
            return redirect('/myapp/admin_changePassword_get/')
    else:
        messages.warning(request, 'incorrect password')
        return redirect('/myapp/admin_changePassword_get/')
def logout_get(request):
    logout(request)
    return redirect('/myapp/login_get/')




# showroom
def showroomsignup_get(request):
    return render(request,'showroom/signup.html')


def showroom_signup(request):
    name = request.POST['name']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    phone = request.POST['phone']
    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(username=email).exists():
        messages.warning(request,'username alredy exists')
        return redirect('/myapp/showroomsignup_get/')
    else:
        license = request.FILES['license']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        fs.save(date, license)
        license_path = fs.url(date)

        photo = request.FILES['photo']
        date2 = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        fs.save(date2, photo)
        photo_path = fs.url(date2)

        user = User.objects.create_user(username=email, password=password, email=email)

        user.groups.add(Group.objects.get(name='showroom'))

        obj = Showroom()
        obj.USER = user
        obj.name = name
        obj.place = place
        obj.pincode = pincode
        obj.district = district
        obj.state = state
        obj.phone = phone
        obj.email = email
        obj.license_proof = license_path
        obj.photo = photo_path
        obj.status = "pending"
        obj.save()

        return redirect('/myapp/login_get/')
def showroomhome(request):
    return render(request,'showroom/showroomhome.html')
def showroomview_profile(request):
    a=Showroom.objects.get(USER=request.user)
    return render(request,'showroom/viewprofile.html',{'data':a})
def editprofile_gets(request):
    a=Showroom.objects.get(USER=request.user)
    return render(request,'showroom/editprofile.html',{'data':a})

def showroom_editprofile(request):
    name = request.POST['name']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    phone = request.POST['phone']
    email = request.POST['email']
    obj = Showroom.objects.get(USER=request.user)

    if User.objects.filter(username=email).exclude(id=request.user.id).exists():
        messages.warning(request, 'Email already exists')
        return redirect('/myapp/showroomview_profile/')

    else:
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            date2 = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
            fs.save(date2, photo)
            photo_path = fs.url(date2)
            obj.photo = photo_path
            obj.save()

        if 'license' in request.FILES:
            license = request.FILES['license']
            fs = FileSystemStorage()
            date = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
            fs.save(date, license)
            license_path = fs.url(date)
            obj.license_proof = license_path
            obj.save()
        request.user.username = email
        request.user.email = email
        request.user.save()

        obj.name = name
        obj.place = place
        obj.pincode = pincode
        obj.district = district
        obj.state = state
        obj.phone = phone
        obj.email = email
        obj.save()

        return redirect('/myapp/showroomview_profile/')

def addservicecenter_get(request):
    return render(request,'showroom/addservicecenter.html')


import random, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.hashers import make_password

def showroom_add_servicecenter(request):
    name = request.POST['name']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    phone = request.POST['phone']
    email = request.POST['email']

    if User.objects.filter(username=email).exists():
        messages.warning(request, "Email already registered")
        return redirect('/myapp/addservicecenter_get/')

    new_pass = str(random.randint(1000, 9999))

    user = User.objects.create(
        username=email,
        email=email,
        password=make_password(new_pass)
    )

    user.groups.add(Group.objects.get(name='servicecenter'))

    photo = request.FILES['photo']
    fs = FileSystemStorage()
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
    fs.save(filename, photo)
    photo_path = fs.url(filename)

    showroom = Showroom.objects.get(USER=request.user)

    ServiceCenter.objects.create(
        USER=user,
        SHOWROOM=showroom,
        name=name,
        place=place,
        pincode=pincode,
        district=district,
        state=state,
        phone=phone,
        email=email,
        photo=photo_path
    )

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "trainingstarted@gmail.com"
        app_password = "nlxasujxgazlbmgz"

        subject = "Service Center Account Created"
        body = f"""
Welcome to EV Portal

Your account has been created by showroom.

Username: {email}
Password: {new_pass}

Login here:
http://127.0.0.1:8000/myapp/login_get/
"""

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        server.quit()

        messages.success(request, "Service center added & password sent to email")

    except Exception as e:
        messages.warning(request, "Service center added but email failed")

    return redirect('/myapp/showroom_view_servicecenter/')

def showroom_view_servicecenter(request):
    data = ServiceCenter.objects.filter(SHOWROOM__USER=request.user)
    return render(request, 'showroom/viewservicecenter.html', {'data': data})
def showroom_delete_servicecenter(request, id):
    sc = ServiceCenter.objects.get(id=id)
    sc.USER.delete()
    sc.delete()
    messages.success(request, "Service center deleted")
    return redirect('/myapp/showroom_view_servicecenter/')
def showroom_edit_servicecenter_get(request,id):
    data = ServiceCenter.objects.get(id=id)
    return render(request, 'showroom/editservicecenter.html', {'data': data})

def showroom_edit_servicecenter_post(request):
    id = request.POST['id']
    name = request.POST['name']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    phone = request.POST['phone']
    email = request.POST['email']

    sc = ServiceCenter.objects.get(id=id)

    if User.objects.filter(username=email).exclude(id=sc.USER.id).exists():
        messages.warning(request, "Email already exists")
        return redirect('/myapp/showroom_edit_servicecenter_get/')

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        fs.save(filename, photo)
        sc.photo = fs.url(filename)

    sc.USER.username = email
    sc.USER.email = email
    sc.USER.save()

    sc.name = name
    sc.place = place
    sc.pincode = pincode
    sc.district = district
    sc.state = state
    sc.phone = phone
    sc.email = email
    sc.save()

    messages.success(request, "Service center updated")
    return redirect('/myapp/showroom_view_servicecenter/')


def showroomviewmodel(request):
    models = VehicleModel.objects.all()

    companies = Company.objects.all()

    return render(request, 'showroom/viewmodel.html', {
        'data': models,
        'companies': companies
    })

def showroomviewvarient(request,id):
    a=VehicleVariant.objects.filter(MODEL_id=id)
    return render(request,'showroom/viewvarient.html',{'data':a})

def addshowroomstock_get(request,id):
    a=VehicleVariant.objects.get(id=id)
    return render(request,'showroom/addstock.html',{'data':a})
def addstock_post(request):
    id=request.POST['id']
    quantity=request.POST['quantity']
    a=ShowroomStock()
    a.SHOWROOM=Showroom.objects.get(USER=request.user)
    a.VARIENT=VehicleVariant.objects.get(id=id)
    a.quantity=quantity
    a.save()
    return redirect('/myapp/showroom_viewstock/')
def showroom_viewstock(request):
    a=ShowroomStock.objects.filter(SHOWROOM__USER=request.user)
    return render(request,'showroom/viewstock.html',{'data':a})
def edit_stock_get(request,id):
    a=ShowroomStock.objects.get(id=id)
    return render(request,'showroom/editstock.html',{'data':a})
def editstock_post(request):
    id=request.POST['id']
    quantity=request.POST['quantity']
    a=ShowroomStock.objects.get(id=id)
    a.quantity=quantity
    a.save()
    return redirect('/myapp/showroom_viewstock/')
def delete_stock(request,id):
    ShowroomStock.objects.get(id=id).delete()
    return redirect('/myapp/showroom_viewstock/')

def addprice_get(request,id):
    a=VehicleVariant.objects.get(id=id)
    return render(request,'showroom/addprice.html',{'data':a})
def addprice_post(request):
    id=request.POST['id']
    price=request.POST['price']
    a=VehiclePrice()
    a.price=price
    a.SHOWROOM=Showroom.objects.get(USER=request.user)
    a.VARIENT=VehicleVariant.objects.get(id=id)
    a.save()
    return redirect('/myapp/showroomview_price/')

def viewprice(request,id):
    prices = VehiclePrice.objects.filter(VARIENT_id=id, SHOWROOM__USER=request.user)
    return render(request, 'showroom/viewprice.html', {
        'data': prices,
        'variant_id': id
    })
def editprice_get(request,id):
    a=VehiclePrice.objects.get(id=id)
    return render(request,'showroom/editprice.html',{'data':a})
def editprice_post(request):
    id=request.POST['id']
    print(id)
    price=request.POST['price']
    a=VehiclePrice.objects.get(id=id)
    a.price=price
    a.save()
    return redirect('/myapp/showroomview_price/')
def deleteprice(request,id):
    VehiclePrice.objects.get(id=id).delete()
    return redirect('/myapp/showroomview_price/')

def showroomview_price(request):
    a=VehiclePrice.objects.filter(SHOWROOM__USER=request.user)
    return render(request,'showroom/vehicleprice.html',{'data':a})

def viewrideRequest(request):
    a=RideRequest.objects.filter(SHOWROOM__USER=request.user)
    return render(request,'showroom/viewriderequest.html',{'data':a})
def acceptride_request(request,id):
    RideRequest.objects.filter(id=id).update(status='accepted')
    return redirect('/myapp/viewrideRequest/')
def rejectride_request(request,id):
    RideRequest.objects.filter(id=id).update(status='rejected')
    return redirect('/myapp/viewrideRequest/')
def view_accepted_rideRequest(request):
    a=RideRequest.objects.filter(SHOWROOM__USER=request.user,status='accepted')
    return render(request,'showroom/viewaccepetedrequest.html',{'data':a})
def view_vehicleBooking(request):
    a=VehicleBooking.objects.filter(SHOWROOM__USER=request.user)
    return render(request,'showroom/viewbooking.html',{'data':a})


def update_vehicle_booking_status(request, id, status):
    try:
        booking = VehicleBooking.objects.get(id=id, SHOWROOM__USER=request.user)

        booking.status = status
        booking.save()

        messages.success(request, "Booking status updated successfully")

    except VehicleBooking.DoesNotExist:
        messages.warning(request, "Booking not found")

    return redirect('/myapp/view_vehicleBooking/')

def showroom_changePassword_get(request):
    return render(request,'showroom/changepassword.html')
def showroom_changePassword_post(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)
            return redirect('/myapp/login_get/')
        else:
            messages.warning(request, 'new password and confirm password must be same')
            return redirect('/myapp/showroom_changePassword_get/')
    else:
        messages.warning(request, 'incorrect password')
        return redirect('/myapp/showroom_changePassword_get/')



# service center

def servicecenterhome(request):
    return render(request, 'ServiceCenter/servicecenterhome.html')
def servicecenterprofile(request):
    a=ServiceCenter.objects.get(USER=request.user)
    return render(request,'ServiceCenter/viewprofile.html',{'data':a})
def servicecenterviewmodels(request):
    b=VehicleModel.objects.all()
    return render(request,'ServiceCenter/viewmodel.html',{'data':b})

def addsparepart_get(request,id):
    a=VehicleModel.objects.get(id=id)
    return render(request,'ServiceCenter/addsparepart.html',{'data':a})
def addsparepart_post(request):
    id=request.POST['id']
    part_name=request.POST['part_name']
    price=request.POST['price']
    stock=request.POST['stock']
    a=SparePart()
    a.MODEL=VehicleModel.objects.get(id=id)
    a.part_name=part_name
    a.price=price
    a.stock=stock
    a.SERVICECENTER=ServiceCenter.objects.get(USER=request.user)
    a.save()
    return redirect('/myapp/viewsparepart/')

def viewsparepart(request):
    a=SparePart.objects.filter(SERVICECENTER__USER=request.user)
    return render(request,'ServiceCenter/viewsparepart.html',{'data':a})
def delete_sparepart(request,id):
    SparePart.objects.get(id=id).delete()
    return redirect('/myapp/viewsparepart/')
def editspareparts_get(request,id):
    a=SparePart.objects.get(id=id)
    return render(request,'ServiceCenter/editsparepart.html',{'data':a})
def editsparepart_post(request):
    id=request.POST['id']
    part_name=request.POST['part_name']
    price=request.POST['price']
    stock=request.POST['stock']
    a=SparePart.objects.get(id=id)
    a.part_name=part_name
    a.price=price
    a.stock=stock
    a.SERVICECENTER=ServiceCenter.objects.get(USER=request.user)
    a.save()
    return redirect('/myapp/viewsparepart/')

def servicevieworders(request):
    a = Order.objects.filter(
        items__SPAREPART__SERVICECENTER__USER=request.user
    ).distinct().order_by('-id')

    return render(request,'ServiceCenter/vieworders.html',{'data':a})


from django.db.models import Exists, OuterRef

from django.db.models import OuterRef, Exists
from .models import ServiceBooking, ServiceBill

def viewservicebooking(request):
    bookings = ServiceBooking.objects.filter(
        SERVICECENTER__USER=request.user
    ).annotate(
        has_bill=Exists(
            ServiceBill.objects.filter(SERVICE=OuterRef('pk'))
        )
    ).order_by('-id')

    return render(request,'ServiceCenter/viewservicebooking.html',{'data':bookings})



def update_service(request,id):
    ServiceBooking.objects.filter(id=id).update(status='finished')
    return redirect('/myapp/viewservicebooking/')
def viewbill(request):
    a=Bill.objects.filter(SERVICEBOOKING__SERVICECENTER__USER=request.user).order_by('-id')
    return render(request,'ServiceCenter/viewbill.html',{'data':a})
def view_review(request):
    a=Review.objects.filter(BILL__SERVICE__SERVICECENTER__USER=request.user).order_by('-id')
    return render(request,'ServiceCenter/viewreview.html',{'data':a})
def servicecenterchangepassword_get(request):
    return render(request,'ServiceCenter/changepassword.html')
def service_changePassword_post(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)
            return redirect('/myapp/login_get/')
        else:
            messages.warning(request, 'new password and confirm password must be same')
            return redirect('/myapp/servicecenterchangepassword_get/')
    else:
        messages.warning(request, 'incorrect password')
        return redirect('/myapp/servicecenterchangepassword_get/')



# user

def userhome(request):
    return render(request,'user/userhome.html')
def usersignup_get(request):
    return render(request,'user/signup.html')

def usersignup_post(request):
    name = request.POST['name']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    phone = request.POST['phone']
    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(username=email).exists():
        messages.warning(request, 'Email already registered')
        return redirect('/myapp/usersignup_get/')

    else:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        fs.save(date, photo)
        photo_path = fs.url(date)

        user = User.objects.create_user(username=email, password=password, email=email)
        user.groups.add(Group.objects.get(name='user'))

        obj = Customer()
        obj.USER = user
        obj.name = name
        obj.place = place
        obj.pincode = pincode
        obj.district = district
        obj.state = state
        obj.phone = phone
        obj.email = email
        obj.photo = photo_path
        obj.save()

        return redirect('/myapp/login_get/')

def viewprofile(request):
    data = Customer.objects.get(USER=request.user)
    return render(request, 'user/viewprofile.html', {'data': data})

def editprofile_get(request):
    data = Customer.objects.get(USER=request.user)
    return render(request, 'user/editprofile.html', {'data': data})

def editprofile_post(request):
    name = request.POST['name']
    place = request.POST['place']
    pincode = request.POST['pincode']
    district = request.POST['district']
    state = request.POST['state']
    phone = request.POST['phone']
    email = request.POST['email']

    obj = Customer.objects.get(USER=request.user)
    user = obj.USER

    if User.objects.filter(username=email).exclude(id=user.id).exists():
        messages.warning(request, "Email already in use")
        return redirect('/myapp/editprofile_get/')

    obj.name = name
    obj.place = place
    obj.pincode = pincode
    obj.district = district
    obj.state = state
    obj.phone = phone
    obj.email = email

    user.username = email
    user.email = email
    user.save()

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        fs.save(date, photo)
        obj.photo = fs.url(date)

    obj.save()

    messages.success(request, "Profile updated successfully")
    return redirect('/myapp/viewprofile/')

def userviewcompany(request):
    a=Company.objects.all()
    return render(request,'user/viewcompany.html',{'data':a})
def userviewmodels(request,id):
    a=VehicleModel.objects.filter(COMPANY_id=id)
    return render(request,'user/viewmodel.html',{'data':a})


def userviewvarients(request,id):
    a=VehicleVariant.objects.filter(MODEL_id=id)
    return render(request,'user/viewvarients.html',{'data':a})

def userviewavailableshowroom(request, id):

    variant = VehicleVariant.objects.get(id=id)

    stocks = ShowroomStock.objects.filter(VARIENT=variant)

    l = []

    for i in stocks:

        qty = int(i.quantity)

        if qty > 0:

            showroom = i.SHOWROOM

            price = VehiclePrice.objects.filter(SHOWROOM=showroom, VARIENT=variant).first()
            price_value = price.price if price else "Not added"

            l.append({
                'showroom_id': showroom.id,
                'name': showroom.name,
                'place': showroom.place,
                'district': showroom.district,
                'phone': showroom.phone,
                'email': showroom.email,
                'photo': showroom.photo,
                'quantity': qty,
                'price': price_value
            })
    print(l)

    return render(request, 'user/view_available_showroom.html', {'data': l, 'variant': variant})

from django.shortcuts import render,redirect
from .models import *

def usersend_riderequest(request, showroom_id, variant_id):

    customer = Customer.objects.get(USER=request.user)

    showroom = Showroom.objects.get(id=showroom_id)
    variant = VehicleVariant.objects.get(id=variant_id)

    check = RideRequest.objects.filter(
        CUSTOMER=customer,
        SHOWROOM=showroom,
        VARIENT=variant,
        status='pending'
    )

    if check.exists():
        return redirect('/myapp/userview_testrideBooking/')

    RideRequest.objects.create(
        CUSTOMER=customer,
        SHOWROOM=showroom,
        VARIENT=variant,
        date=datetime.now().today(),
        status='pending'
    )

    return redirect('/myapp/userview_testrideBooking/')

def userview_testrideBooking(request):
    a=RideRequest.objects.filter(CUSTOMER__USER=request.user)
    return render(request,'user/viewriderequest.html',{'data':a})


from django.db import transaction
@transaction.atomic
def user_book_vehicle(request, showroom_id, variant_id):

    if request.method == "POST":

        customer = Customer.objects.get(USER=request.user)
        showroom = Showroom.objects.get(id=showroom_id)
        variant = VehicleVariant.objects.get(id=variant_id)

        stock = ShowroomStock.objects.select_for_update().get(
            SHOWROOM=showroom,
            VARIENT=variant
        )

        current_stock = int(stock.quantity)

        if current_stock <= 0:
            return redirect('/myapp/userviewbooking/')

        if VehicleBooking.objects.filter(
            CUSTOMER=customer,
            SHOWROOM=showroom,
            VARIENT=variant,
            status='pending'
        ).exists():
            return redirect('/myapp/userviewbooking/')

        VehicleBooking.objects.create(
            CUSTOMER=customer,
            SHOWROOM=showroom,
            VARIENT=variant,
            date=datetime.now().today(),
            status='pending'
        )

        current_stock -= 1
        stock.quantity = str(current_stock)
        stock.save()

        return redirect('/myapp/userviewbooking/')

def userviewbooking(request):
    a=VehicleBooking.objects.filter(CUSTOMER__USER=request.user)
    return render(request,'user/viewbooking.html',{'data':a})
def userviewspareparts(request):

    centers = ServiceCenter.objects.all()
    servicecenter_id = request.GET.get('servicecenter')

    if servicecenter_id:
        parts = SparePart.objects.filter(SERVICECENTER_id=servicecenter_id)
    else:
        parts = SparePart.objects.all()

    # convert stock to integer flag
    part_list = []
    for p in parts:
        part_list.append({
            'obj': p,
            'stock': int(p.stock),
            'is_high': int(p.stock) > 5
        })

    return render(request,'user/viewsparepart.html',{
        'data':part_list,
        'centers':centers,
        'selected_center':servicecenter_id
    })


from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import json
from django.http import JsonResponse

def add_to_cart(request, id):
    customer = Customer.objects.get(USER=request.user)
    part = SparePart.objects.get(id=id)

    qty = int(request.POST.get('qty', 1))

    existing = Cart.objects.filter(CUSTOMER=customer, SPAREPART=part).first()

    if existing:
        existing.quantity += qty
        existing.save()
    else:
        Cart.objects.create(
            CUSTOMER=customer,
            SPAREPART=part,
            quantity=qty
        )

    return redirect('/myapp/view_cart/')

def view_cart(request):
    customer = Customer.objects.get(USER=request.user)
    items = Cart.objects.filter(CUSTOMER=customer)

    total = 0
    for i in items:
        total += int(i.quantity) * int(i.SPAREPART.price)

    return render(request, 'user/viewcart.html', {'data': items, 'total': total})

# INCREASE QTY
def increase_qty(request, id):
    customer = Customer.objects.get(USER=request.user)
    item = Cart.objects.get(id=id, CUSTOMER=customer)

    item.quantity = int(item.quantity) + 1
    item.save()
    return redirect('/myapp/view_cart/')


# DECREASE QTY
def decrease_qty(request, id):
    customer = Customer.objects.get(USER=request.user)
    item = Cart.objects.get(id=id, CUSTOMER=customer)

    if int(item.quantity) > 1:
        item.quantity = int(item.quantity) - 1
        item.save()
    else:
        item.delete()  # remove item if qty becomes 0

    return redirect('/myapp/view_cart/')
def place_order(request):

    customer = Customer.objects.get(USER=request.user)
    items = Cart.objects.filter(CUSTOMER=customer)

    if not items:
        return redirect('/myapp/view_cart/')

    total = 0
    for i in items:
        total += int(i.quantity) * int(i.SPAREPART.price)

    order = Order.objects.create(
        CUSTOMER=customer,
        amount=total,
        status='pending',
        date=datetime.now()
    )

    # store items permanently
    for i in items:
        OrderItem.objects.create(
            ORDER=order,
            SPAREPART=i.SPAREPART,
            quantity=i.quantity,
            price=i.SPAREPART.price
        )

    return render(request, 'user/payment.html', {
        'amount': int(total) * 100,
        'id': order.id,
        'razorpay_api_key': 'rzp_test_MJOAVy77oMVaYv',
        'currency': 'INR'
    })


def pay_existing_order(request, id):

    order = Order.objects.get(id=id)

    # security check
    if order.CUSTOMER.USER != request.user:
        return redirect('/myapp/view_cart/')

    if order.status == "paid":
        return redirect('/myapp/vieworders/')

    return render(request, 'user/payment.html', {
        'amount': int(order.amount) * 100,
        'id': order.id,
        'razorpay_api_key': 'rzp_test_MJOAVy77oMVaYv',
        'currency': 'INR'
    })
def payment_success(request):

    if request.method == "POST":

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        if order.status == "paid":
            return redirect('/myapp/view_cart/')

        order.status = "paid"
        order.save()

        # reduce stock using order items
        for item in order.items.all():
            spare = item.SPAREPART
            spare.stock = str(int(spare.stock) - int(item.quantity))
            spare.save()

        # clear cart
        Cart.objects.filter(CUSTOMER=order.CUSTOMER).delete()

        send_mail(
            'Order Confirmed',
            f'Your order #{order.id} has been placed successfully.',
            settings.EMAIL_HOST_USER,
            [order.CUSTOMER.USER.email],
            fail_silently=True
        )

        return redirect('/myapp/order_status/')


def order_status(request):
    customer = Customer.objects.get(USER=request.user)
    orders = Order.objects.filter(CUSTOMER=customer).order_by('-date')
    return render(request, 'user/vieworders.html', {'data': orders})


def userview_servicecenter(request):
    a=ServiceCenter.objects.all()
    return render(request,'user/service center.html',{'data':a})

def book_service(request, id):
    center = ServiceCenter.objects.get(id=id)
    return render(request, 'user/book_service.html', {'center': center})
def book_service_post(request):

    customer = Customer.objects.get(USER=request.user)

    center_id = request.POST['center']
    model = request.POST['model']
    issue = request.POST['issue']
    date = request.POST['date']

    ServiceBooking.objects.create(
        CUSTOMER=customer,
        SERVICECENTER_id=center_id,
        vehicle_model=model,
        issue=issue,
        service_date=date,
        status='booked'
    )

    return redirect('/myapp/view_upcoming_services/')

def view_upcoming_services(request):
    customer = Customer.objects.get(USER=request.user)

    services = ServiceBooking.objects.filter(
        CUSTOMER=customer,
        status='booked'
    ).order_by('service_date')

    return render(request,'user/upcoming_services.html',{'data':services})
def view_service_history(request):
    customer = Customer.objects.get(USER=request.user)

    bills = ServiceBill.objects.filter(
        SERVICE__CUSTOMER=customer
    ).select_related('SERVICE','SERVICE__SERVICECENTER').order_by('-id')

    return render(request,'user/service_history.html',{'data':bills})

def pay_bill(request, id):

    bill = ServiceBill.objects.get(id=id)

    return render(request, 'user/bill_payment.html', {
        'amount': int(bill.total_amount) * 100,
        'display_amount': bill.total_amount,
        'id': bill.id,
        'currency': 'INR',
        'razorpay_api_key': 'rzp_test_MJOAVy77oMVaYv'
    })

def bill_payment_success(request):

    bill_id = request.POST.get('bill_id')
    bill = ServiceBill.objects.get(id=bill_id)

    if bill.status == "paid":
        return redirect('/myapp/view_service_history/')

    bill.status = "paid"
    bill.save()

    return redirect('/myapp/view_service_history/')


def add_review(request, id):

    bill = ServiceBill.objects.get(id=id)

    # Allow only if paid
    if bill.status != "paid":
        return redirect('/myapp/view_service_history/')

    # Prevent duplicate review
    if Review.objects.filter(BILL=bill).exists():
        return redirect('/myapp/view_service_history/')

    return render(request,'user/add_review.html',{'bill':bill})
from datetime import datetime

def add_review_post(request):

    customer = Customer.objects.get(USER=request.user)

    bill_id = request.POST['bill']
    rating = request.POST['rating']
    comment = request.POST['comment']

    bill = ServiceBill.objects.get(id=bill_id)

    # Double protection
    if bill.status != "paid":
        return redirect('/myapp/view_service_history/')

    if Review.objects.filter(BILL=bill).exists():
        return redirect('/myapp/view_service_history/')

    Review.objects.create(
        CUSTOMER=customer,
        BILL=bill,
        rating=rating,
        comment=comment,
        date=datetime.now().date()
    )

    return redirect('/myapp/view_service_history/')


def generate_bill(request, id):
    booking = ServiceBooking.objects.get(id=id)

    if request.method == "POST":
        labor = int(request.POST.get('labor'))
        spare = int(request.POST.get('spare'))
        total = labor + spare

        ServiceBill.objects.create(
            SERVICE=booking,
            labor_charge=labor,
            spare_charge=spare,
            total_amount=total
        )

        booking.status = "completed"
        booking.save()

        return redirect('/myapp/viewservicebooking/')

    return render(request, 'ServiceCenter/generate_bill.html', {'data': booking})

def view_bill(request, id):
    try:
        # Try to get the service booking
        booking = ServiceBooking.objects.get(id=id)
    except ServiceBooking.DoesNotExist:
        # Redirect if booking not found
        return redirect('viewservicebooking')

    # Get the linked ServiceBill using the related_name 'Bill'
    bill = getattr(booking, 'Bill', None)  # Returns None if no bill exists

    if not bill:
        # Redirect if no bill exists
        return redirect('viewservicebooking')

    return render(request, 'ServiceCenter/viewbill.html', {'bill': bill, 'booking': booking})


def user_view_services(request):
    customer = Customer.objects.get(USER=request.user)
    bookings = ServiceBooking.objects.filter(CUSTOMER=customer).order_by('-id')
    return render(request, 'User/view_services.html', {'data': bookings})

def user_view_bill(request, id):
    booking = ServiceBooking.objects.get(id=id)
    bill = booking.bill
    return render(request, 'User/user_view_bill.html', {'bill': bill})



def user_changePassword_get(request):
    return render(request,'user/changepassword.html')
def user_changePassword_post(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)
            return redirect('/myapp/login_get/')
        else:
            messages.warning(request, 'new password and confirm password must be same')
            return redirect('/myapp/user_changePassword_get/')
    else:
        messages.warning(request, 'incorrect password')
        return redirect('/myapp/user_changePassword_get/')


def send_feedback(request):
    return render(request,'user/send_feedback.html')
from datetime import date

def send_feedback_post(request):
    customer = Customer.objects.get(USER=request.user)

    message = request.POST['message']

    Feedback.objects.create(
        CUSTOMER=customer,
        message=message,
        status='pending',
        reply='Not replied yet',
        date=date.today()
    )

    return redirect('/myapp/view_feedback/')

def view_feedback(request):
    customer = Customer.objects.get(USER=request.user)

    data = Feedback.objects.filter(CUSTOMER=customer).order_by('-id')

    return render(request,'user/view_feedback.html',{'data':data})


def admin_view_feedback(request):
    data = Feedback.objects.all().order_by('-id')
    return render(request,'admin/view_feedback.html',{'data':data})
def reply_feedback(request,id):
    fb = Feedback.objects.get(id=id)

    if request.method == "POST":
        fb.reply = request.POST['reply']
        fb.status = 'replied'
        fb.save()
        return redirect('/myapp/admin_view_feedback/')

    return render(request,'admin/reply_feedback.html',{'data':fb})




def customer_order_history(request):
    customer = request.user.customer  
    orders = Order.objects.filter(CUSTOMER=customer).order_by('-date')
    return render(request, 'user/orders_history.html', {'orders': orders})

def forgot_password_get(request):
    return render(request,'forgetpassword.html')

def forgotpassword_post(request):
    email = request.POST['email']

    if User.objects.filter(username=email).exists():

        import random
        new_pass = random.randint(00000, 99999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("leagaladvisorteam@gmail.com", " eugnxtyylwtqwlav")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)
        server.quit()

        user = User.objects.get(username=email)
        user.set_password(str(new_pass))
        user.save()

        return redirect('/myapp/login_get/')
    else:
        messages.warning(request, 'email not  exists')
        return redirect('/myapp/forgot_password_get/')
