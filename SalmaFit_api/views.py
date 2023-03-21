from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from django.views import View
from rest_framework.views import APIView
from django.db.models import Count
from SalmaFit_api.serializers import *
from .models import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from pyfcm import FCMNotification
from django.core.mail import send_mail
import requests
import random
import json



#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


class EmailVerificationView(APIView):
    def post(self, request, format=None):
        serializer = UserEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            if not User.objects.filter(email=email):
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                send_mail(
                'Salma Style',
                f'Your OTP For Email Verification is {otp}. Valid For Only 2 Minutes',
                ('EMAIL_HOST_USER'),
                [email],
                fail_silently=False,
                )
                return Response({'status':'True', 'message':'OTP Sent. Valid For Only 2 Minutes'})
            return Response({'status':'False', 'message':'Email Already Exits'})
        return Response({'status':'False', 'message':'404 Bad Request', 'errors':serializer.errors})


class VerifyEmailView(APIView):
    def post(self, request, format=None):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.data['verify_email_otp']
            try:
                if request.session['otp'] == otp:
                    return Response({'status':'True', 'message':'Your Email Is Verified'})
                return Response({'status':'False', 'message':'Your Email Is Not Verified'})
            except KeyError:
                return Response({'status':'False', 'message':'OTP Expired, Generate Again'})
        return Response({'status':'False', 'message':'404 Bad Request', 'errors':serializer.errors})
    


class UserRegistration(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'True', 'message':'User Registration Is Succesful'})
        return Response({'status':'False', 'message':'Email or Phone Already Exists', 'errors':serializer.errors})


class UserLoginView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            device_token = serializer.data.get('device_token')
            user = authenticate(email=email, password=password)
            if user is not None:
                device = User.objects.filter(email=email)
                device.update(device_token=device_token)
                token = get_tokens_for_user(user)
                return Response({'status':'True', 'message':'User Login Succesful', 'token':token}) 
            return Response({'status':'False', 'message':'Email or Password is not Valid or User is Deactivated'})
        return Response({'status':'False', 'message':'User Login Data Is Not Valid'})


class UserProfileView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(instance=request.user)
        return Response({'status':'True', 'message':'View Your Profile', "data": serializer.data})    
    def put(self, request, format=None):
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'True', 'message':'User Profile Changed Succesfully'})
        return Response({'status':'False', 'message':'Email or Phone Already Exists'})


class UserProfileDeactivateView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        User.objects.filter(email=request.user.email).update(is_active=False)
        return Response({'status':'True', 'message':'User Profile Deactivated Succesfully'})



class UserChangePasswordView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            return Response({'status':'True', 'message':'Password Changed Successfully'})
        return Response({'status':'False', 'message':'Old Password Is Not Correct'})


class SendPasswordResetEmailView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status':'True', 'message':'Password Reset Link Send. Please Check Your Email'})
        return Response({'status':'False', 'message':'Email Is Not Valid'})


class UserPasswordResetView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid():
            return Response({'status':'True', 'message':'Password Reset Successfully'})
        return Response({'status':'False', 'message':'Password Is Not Valid'})


class UserLogoutView(generics.GenericAPIView):
    # renderer_classes = [UserRenderer]
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'True', 'message':'User Is Logout'})
        return Response({'status':'False', 'message':'404 Bad Request'})


# class ProductsView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, barcode_number=None, format=None):
#         if Products.objects.filter(barcode_number=barcode_number).exists():
#             products = Products.objects.get(barcode_number=barcode_number)
#             serializer = ProductsSerializer(products)
#             return Response({'status':'True', 'message':'Please View Product Details', "data": serializer.data})
#         url = "https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key=75a4mul7klwbu5h1zcq4olmc4gwgyj".format(barcode=barcode_number)
#         payload={}
#         headers = {
#         'Cookie': '__cf_bm=jORoibK.OpuHdTtoJvYs9nfmy0pdVidzI7jbtCSzCns-1655374449-0-ARCELIzHSZ1+jPkxRVtrL0OjKBm6Ca2oFkRqMjo553djKPDWLed687J8QL/MRsu7X9ceWbehixbbc6WRB5r07hE1IrpxFwXZp14dZiiH/qzj; bl_csrf=e1f70d827ab01308fbb02a57da157f52; bl_session=069nkseoni3l8la6k0kgfff461hasamh; __cflb=0H28uyvJ4CKpQyt4K4sAVoNGmQD7bdrdPmHNCQwF2fX'
#         }
#         response = requests.request("GET", url, headers=headers, data=payload)
#         text_data = response.text
#         json_data = json.loads(text_data)
#         product = json_data['products'][0]
#         products = Products.objects.create(user=request.user,barcode_number=product['barcode_number'],barcode_formats=product['barcode_formats'],title=product['title'],brand=product['brand'],ingredients=product['ingredients'],nutrition_facts=product['nutrition_facts'],energy_efficiency_class=product['energy_efficiency_class'],color=product['color'],description=product['description'],features=product['features'],images=product['images'],last_update=product['last_update'])
#         stores_data = json_data['products'][0]['stores']
#         for i in stores_data:
#             stores = Stores.objects.create(user=request.user,product=products,name=i['name'],country=i['country'],currency=i['currency'],price=i['price'],link=i['link'],last_update=i['last_update'])
#         serializer = ProductsSerializer(products)
#         return Response({'status':'True', 'message':'Please View Product Details', "data": serializer.data})


# class ProductsView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, barcode_number=None, format=None):
#         if Products.objects.filter(barcode_number=barcode_number).exists():
#             products = Products.objects.get(barcode_number=barcode_number)
#             serializer = ProductsSerializer(products)
#             return Response({'status':'True', 'message':'Please View Your Product Details', "data": serializer.data})
#         return Response({'status':'False', 'message':'This has not scanned before in Salma Style. Do You Want To Add ?'})
#     def post(self, request, barcode_number=None, format=None):
#         if not Products.objects.filter(barcode_number=barcode_number).exists():
#             # product_image = UserProductImages.POST['product_image']
#             # nutrition_facts_image = UserProductImages.POST['nutrition_facts_image']
#             # ingredients_image = UserProductImages.POST['ingredients_image']
#             # UserProductImages.objects.create(user=request.user, product_image=product_image, nutrition_facts_image=nutrition_facts_image, ingredients_image=ingredients_image)
#             serializer = UserProductImagesSerializer(instance=request.user, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'status':'True', 'message':'Product Added Succesfully'})
#             return Response({'status':'False','message':'Image Is Not Valid'})
#         return Response({'status':'False','message':'Product Is Arleady In The System'})


class CountryCodeView(APIView):
    def get(self, request, format=None):
        country_code = CountryCode.objects.all()
        serializer = CountryCodeSerializer(country_code, many=True)
        return Response({'status':'True', 'message':'Country Code Lists', "data": serializer.data})


class PhoneVerificationView(APIView):
    def post(self, request, format=None):
        serializer = UserPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data['phone']
            user = User.objects.filter(phone=phone)
            if user.exists():
                return Response({'status':'True', 'message':'Phone Is Valid'})
            return Response({'status':'False', 'message':'Phone Does Not Exists'})
        return Response({'status':'False', 'message':'404 Bad Request', 'errors':serializer.errors})


class ResetPassword(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data['phone']
            if User.objects.filter(phone=phone).exists():
                user = User.objects.get(phone=phone)
                user.set_password(request.data['password'])
                user.save()
                return Response({'status':'True', 'message':'Reset Password Succesful'})
            return Response({'status':'False', 'message':'Phone Does Not Exists'})
        return Response({'status':'False', 'message':'404 Bad Request', 'errors':serializer.errors})


class ProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        # barcode = ProductSerializer(data=request.data)
        # if barcode.is_valid():
            # number = barcode.data.get('barcode')
            barcode_number = request.data.get('barcode')
            if Products.objects.filter(barcode_number=barcode_number).exclude(Q(status='Pending')|Q (status='Not Clear Photos')).exists():
                products = Products.objects.get(barcode_number=barcode_number)
                serializer = ProductsSerializer(products)
                return Response({'status':'True', 'message':'Please View Your Product Details', "data": serializer.data})
            elif Products.objects.filter(status='Not Clear Photos', barcode_number=barcode_number).exists():
                products = Products.objects.get(barcode_number=barcode_number)
                serializer = ProductsSerializer(products)
                return Response({'status':'True', 'message':'This Product has has not clear photos to review. Please wait for Review by Salma Style', "data": serializer.data})
            elif Products.objects.filter(status='Pending', barcode_number=barcode_number).exists():
                return Response({'status':'True', 'message':'This Product is in Pending. Please wait for Review by Salma Style'})
            else:
                return Response({'status':'False', 'message':'This Product Is Not In The Salma Style Currently. Do You Want To Add?',
                'message_in_english':'The product has been removed by Salma Style', 'message_in_farsi':'این محصول توسط سلما استایل حذف شده است'})
        # return Response({'status':'False','message':'Enter Barcode Number'})


# class ProductsAddView(APIView):
#     # renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         barcode_number = request.data.get('barcode')
#         serializer = UserProductImagesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user = request.user, barcode_number=barcode_number)
#             return Response({'status':'True', 'message':'Product Added Succesfully'})
#         return Response({'status':'False','message':'Photos Are Not Valid', 'data':serializer.errors})


class ProductsAddView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        barcode = request.data.get('barcode')
        barcode_image = request.data.get('barcode_image')
        product_image = request.data.get('product_image')
        nutrition_facts_image = request.data.get('nutrition_facts_image')
        ingredients_image = request.data.get('ingredients_image')
        if barcode:
            if (barcode_image and product_image) and (nutrition_facts_image and ingredients_image):
                if not Products.objects.filter(barcode_number=barcode).exists():
                    Products.objects.create(user = request.user, barcode_number=barcode, barcode_image=barcode_image, product_image=product_image, nutrition_facts_image=nutrition_facts_image, ingredients_image=ingredients_image)
                    return Response({'status':'True', 'message':'Product Added Succesfully'})
                return Response({'status':'False', 'message':'Product Is Already In Salma Style'})
            return Response({'status':'False', 'message':'Provide All the Images of Product'})
        return Response({'status':'False', 'message':'Provide Barcode Number'})


class RecentProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_products = Products.objects.filter(user=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')[:50]
        serializer = ProductsSerializer(my_products, many=True)
        return Response({'status':'True', 'message':'Recent 50 Products Details', "data": serializer.data})


class PendingProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_products = Products.objects.filter(Q(status='Pending') | Q(status='Not Clear Photos'), user=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')[:50]
        serializer = ProductsSerializer(my_products, many=True)
        return Response({'status':'True', 'message':"User's Pending Products Details", "data": serializer.data})


class EditProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        id = request.data.get('id')
        if Products.objects.filter(id=id).exists():
            images = Products.objects.get(id=id)
            serializer = ProductsSerializer(images, data=request.data, partial=True)
            if serializer.is_valid():
                barcode = images.barcode_number
                product_image = images.product_image
                user = images.user
                device_token = images.user.device_token
                Notifications.objects.create(title = barcode+' Added', عنوان =barcode+' اضافه کرده', barcode = barcode, product_image = product_image,
                                            message='Hello! Your product has been added to the system by another user, please wait for review.',
                                            پیام='سلام! محصول شما توسط کاربر دیگری به سیستم اضافه شده است، لطفا منتظر بررسی باشید.').recipient.add(user)
                if device_token:
                    # push_service = FCMNotification(api_key="AAAAoMs1f38:APA91bHqV88hO4VWjZ3Vkj1xNaFN4H6AM2PvyWdOCmsRDDei_-IEMNjQ6MeqSyC7ukM4sqAoE_IvYPeGzj8ajnn9sCQleiQzX4UQGioZ1sl0ldlz6PjpaoR1W-2W7utcsqvUFM6PZ6EI")
                    push_service = FCMNotification(api_key="AAAAj38eBRc:APA91bGYlxdKEKkdMSnoqZ-gR9fu8zvDX87rtbYaa1K7HLiOcFqzmDqZtrjMrW0mo5AP1HjFhJUaeHN2pSt-rRlQhD7pWYcW1Piiga6G6YySYt0wufqeMEh7n7mUYFAsYwNE83tPmRMD")
                    registration_id = device_token
                    message_title = barcode+" Added"
                    message_body = "Hello! Your product has been added to the system by another user, please wait for review."
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                    print (result)
                serializer.save(user=request.user, status='Pending')
                return Response({'status':'True', 'message':'Product Detail Updated Successfully'})
            return Response({'status':'False', 'message':'Product Detail Is Not Valid'})
        return Response({'status':'False', 'message':'You Can Not Change The Product Detail Now'})


class RejectedProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_products = Products.objects.filter(status='Rejected', user=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')[:50]
        serializer = ProductsSerializer(my_products, many=True)
        return Response({'status':'True', 'message':'Recent 50 Rejected Products Details', "data": serializer.data})


class ApprovedProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_products = Products.objects.filter(status='Approved', user=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')[:50]
        serializer = ProductsSerializer(my_products, many=True)
        return Response({'status':'True', 'message':'Recent 50 Approved Products Details', "data": serializer.data})


class OccasionallyProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_products = Products.objects.filter(status='Occasionally', user=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')[:50]
        serializer = ProductsSerializer(my_products, many=True)
        return Response({'status':'True', 'message':'Recent 50 Occasionally Products Details', "data": serializer.data})


class RejectedWhileDietingProductsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_products = Products.objects.filter(status='Rejected While Dieting', user=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')[:50]
        serializer = ProductsSerializer(my_products, many=True)
        return Response({'status':'True', 'message':'Recent 50 Rejected While Dieting Products Details', "data": serializer.data})


class NotificationsView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        if Notifications.objects.filter(recipient=request.user).exists():
            notification = Notifications.objects.filter(recipient=request.user).order_by('-created_at__year','-created_at__month','-created_at__day','-created_at__hour','-created_at__minute','-created_at__second')
            count = notification.aggregate(Count('message'))
            serializer = NotificationsSerializer(notification, many=True)
            return Response({'status':'True', "count":count, 'message':'All Notifications', "data": serializer.data})
        return Response({'status':'False', 'message':'Notification Is Unavailable'})
    def post(self, request, format=None):
        if Notifications.objects.filter(recipient=request.user).exists():
            notification = Notifications.objects.filter(recipient=request.user)
            for i in notification:
                i.recipient.remove(request.user)
            return Response({'status':'True', 'message':'Notifications Are Cleared'})
        return Response({'status':'False', 'message':'Notification Is Unavailable'})


# class NotificationDetailView(APIView):
#     # renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#             id = request.data.get('id')
#             if Notifications.objects.filter(id=id).exists():
#                 notification = Notifications.objects.get(id=id)
#                 serializer = NotificationsSerializer(notification)
#                 return Response({'status':'True', 'message':'Clicked Notification', "data": serializer.data})
#             return Response({'status':'False', 'message':'Notification Is Unvailable'})


class NotificationRemoveView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        id = request.data.get('id')
        if Notifications.objects.filter(id=id, recipient=request.user).exists():
            notification = Notifications.objects.get(id=id)
            notification.recipient.remove(request.user)
            return Response({'status':'True', 'message':'Notification Is Deleted'})
        return Response({'status':'False', 'message':'Notification Is Unavailable'})


class AboutUsView(View):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        if AboutUs.objects.filter(language='English').exists():
            about_us = AboutUs.objects.filter(language='English')
            return render (request, 'aboutus.html', {'about_us':about_us})
        about_us = AboutUs.objects.filter(language='فارسی')
        return render (request, 'aboutusfarsi.html', {'about_us':about_us})


class FarsiAboutUsView(View):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        if AboutUs.objects.filter(language='فارسی').exists():
            about_us = AboutUs.objects.filter(language='فارسی')
            return render (request, 'aboutusfarsi.html', {'about_us':about_us})
        about_us = AboutUs.objects.filter(language='English')
        return render (request, 'aboutus.html', {'about_us':about_us})


class TermsAndConditionsView(View):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        if TermsAndConditions.objects.filter(language='English').exists():
            terms_and_conditions = TermsAndConditions.objects.filter(language='English')
            # serializer = TermsAndConditionsSerializer(terms_and_conditions, many=True)
            # return Response({'status':'True', 'message':'Terms And Conditions', "data": serializer.data})
            return render (request, 'terms.html', {'terms_and_conditions':terms_and_conditions})
        terms_and_conditions = TermsAndConditions.objects.filter(language='فارسی')
        return render (request, 'termsfarsi.html', {'terms_and_conditions':terms_and_conditions})


class FarsiTermsAndConditionsView(View):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        if TermsAndConditions.objects.filter(language='فارسی').exists():
            terms_and_conditions = TermsAndConditions.objects.filter(language='فارسی')
            return render (request, 'termsfarsi.html', {'terms_and_conditions':terms_and_conditions})
        terms_and_conditions = TermsAndConditions.objects.filter(language='English')
        return render (request, 'terms.html', {'terms_and_conditions':terms_and_conditions})


class PrivacyPolicyView(View):
    def get(self, request):
        privacy_policy = PrivacyPolicy.objects.all()
        return render (request, 'privacy.html', {'privacy_policy':privacy_policy})