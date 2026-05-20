from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    USER = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    photo = models.CharField(max_length=500)
    place = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
class Company(models.Model):
    name = models.CharField(max_length=150)
    logo = models.CharField(max_length=500)
    description = models.TextField()
class VehicleModel(models.Model):
    COMPANY = models.ForeignKey(Company, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=150)
    fuel_type = models.CharField(max_length=50)
class VehicleVariant(models.Model):
    MODEL = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=150)
    engine_cc = models.CharField(max_length=100)
    mileage = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    photo = models.CharField(max_length=500)
class Showroom(models.Model):
    USER = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    license_proof = models.CharField(max_length=500)
    status = models.CharField(max_length=100, default="pending")
    photo = models.CharField(max_length=500)

class ShowroomStock(models.Model):
    SHOWROOM = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    VARIENT = models.ForeignKey(VehicleVariant, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
class VehiclePrice(models.Model):
    SHOWROOM = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    VARIENT = models.ForeignKey(VehicleVariant, on_delete=models.CASCADE)
    price=models.CharField(max_length=100)
class ServiceCenter(models.Model):
    USER = models.OneToOneField(User, on_delete=models.CASCADE)
    SHOWROOM = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    photo = models.CharField(max_length=500)

class SparePart(models.Model):
    SERVICECENTER = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    MODEL = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=150)
    price = models.CharField(max_length=100)
    stock = models.CharField(max_length=100)

class RideRequest(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    SHOWROOM = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    VARIENT = models.ForeignKey(VehicleVariant, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100, default='pending')

class VehicleBooking(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    SHOWROOM = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    VARIENT = models.ForeignKey(VehicleVariant, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100,default='pending')

class ServiceBooking(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    SERVICECENTER = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=150)
    issue = models.TextField()
    service_date = models.DateField()
    status = models.CharField(max_length=100,default='booked')

class Bill(models.Model):
    SERVICEBOOKING = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default='ordered')
    date = models.DateField()
class ServiceBill(models.Model):
    SERVICE = models.OneToOneField(ServiceBooking, on_delete=models.CASCADE, related_name='Bill')
    labor_charge = models.IntegerField()
    spare_charge = models.IntegerField()
    total_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="unpaid")


class Cart(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    SPAREPART = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    date = models.DateTimeField()


class OrderItem(models.Model):
    ORDER = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    SPAREPART = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    BILL = models.OneToOneField(ServiceBill, on_delete=models.CASCADE)
    rating = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateField()


class Feedback(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    status=models.CharField(max_length=100,default='pending')
    reply = models.TextField()
    date = models.DateField()








