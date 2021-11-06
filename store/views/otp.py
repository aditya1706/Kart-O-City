from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


def checkotp(request):
    
    email = request.POST.get('email')
    otp = request.POST.get('otp')

    customer = Customer.get_customer_by_email(email)

    phone = customer.phone

    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
    OTP = pyotp.TOTP(key,interval = 50)  # TOTP Model 
    print("Idhar otp: ",OTP.now())
    if OTP.verify(otp):  # Verifying the OTP
        request.session['customer'] = customer.id
        return redirect('homepage')
    else:
    	error_message = 'incorrect otp'
    	return render(request, 'login.html', {'error': error_message})


def checkotpmanageprofile(request):
    pass