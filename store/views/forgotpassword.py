from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from store.models.product import Product
from store.models.seller import Seller
from store.models.orders import Order
from store.templates.captcha import MyForm
import razorpay
from django.views import  View
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
import smtplib, ssl
from email.mime.text import MIMEText
from store.templates.captcha import MyForm
from kartocity.settings import EMAIL_PASSWORD
from kartocity.settings import EXPIRY_TIME
from kartocity.settings import EMAIL_ADDR


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

class sendOTP:
    @staticmethod
    def otpsend(email,phone,otp):
        port = 465 
        password = EMAIL_PASSWORD
        sender_email = EMAIL_ADDR
        receiver_email = email
        message = MIMEText("Hi there,\n\n"+otp+" is your Kart-O-City forgot password OTP")
        message['Subject'] = 'Kart-O-City Login OTP'
        message['From'] = EMAIL_ADDR
        message['To'] = email

        server = smtplib.SMTP_SSL("smtp.gmail.com", port)
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], message.as_string())
        server.quit()



def forgotcustomer(request):
	return render(request, 'forgotcustomer.html', {})
	

def forgotseller(request):
	return render(request, 'forgotseller.html', {})

def sendotpforgotcustomer(request):
	email = request.POST.get('email')
	customer = Customer.get_customer_by_email(email)
	if customer:
		phone = customer.phone
		keygen = generateKey()
		key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
		OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
		print("otp ",OTP.now())
		otpobj = sendOTP()
		otpobj.otpsend(email,phone,OTP.now())
		return render(request, 'otpforgotcustomer.html', {'email':email})
	else:
		error_msg = "Email is not registered!"
		return render(request, 'login.html', {'error':error_msg})
	

def sendotpforgotseller(request):
	email = request.POST.get('email')
	customer = Seller.get_seller_by_email(email)
	if customer:
		phone = customer.phone
		keygen = generateKey()
		key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
		OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
		print("otp ",OTP.now())
		otpobj = sendOTP()
		otpobj.otpsend(email,phone,OTP.now())
		return render(request, 'otpforgotseller.html', {'email':email})
	else:
		error_msg = "Email is not registered!"
		return render(request, 'sellerLogin.html', {'error':error_msg})


def newpasswordcustomer(request):
	email = request.POST.get('email')
	password1 = request.POST.get('pswrd_1')
	password2 = request.POST.get('pswrd_2')
	if password1==password2:
		customer = Customer.get_customer_by_email(email)
		customer.password = make_password(password1)
		confirm_message = "Password Updated"
		customer.register()
		return render(request, 'login.html', {'confirm_message':confirm_message,'form':MyForm})
	else:
		error_msg = 'Password did not match'
		return render(request, 'newpasswordcustomer.html', {'email':email,'error_message':error_msg}) 

def newpasswordseller(request):
	email = request.POST.get('email')
	password1 = request.POST.get('pswrd_1')
	password2 = request.POST.get('pswrd_2')
	if password1==password2:
		customer = Seller.get_seller_by_email(email)
		customer.password = make_password(password1)
		confirm_message = "Password Updated"
		customer.register()
		return render(request, 'sellerLogin.html', {'confirm_message':confirm_message,'form':MyForm})
	else:
		error_msg = 'Password did not match'
		return render(request, 'newpasswordseller.html', {'email':email,'error_message':error_msg}) 

