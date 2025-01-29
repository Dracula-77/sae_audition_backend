from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,HttpResponse
from rest_framework import status
from .models import AuditionData
from .serializers import AuditionDataSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OTP
from twilio.rest import Client
from django.conf import settings
from .serializers import SendOtpSerializer, VerifyOtpSerializer
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
import random
from .serializers import SendOtpSerializer
from .models import OTP
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  
class AuditionDataView(APIView):
    def post(self, request):
        serializer = AuditionDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                    return Response(
                        {"roll": ["This roll number already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        data = AuditionData.objects.all()
        serializer = AuditionDataSerializer(data, many=True)
        return Response(serializer.data)

class RegisterUserView(APIView):  # Separate view for user registration
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)
class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        # Validate the incoming data
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
class DeleteObjectView(APIView):
    def delete(self, request, pk):
        try:
            obj = AuditionData.objects.get(pk=pk)
            obj.delete()
            return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except AuditionData.DoesNotExist:
            raise NotFound(detail="Object not found")
class SearchView(APIView):
    def get(self, request):
        Namequery = request.GET.get('Namequery', '')
        Rollquery = request.GET.get('Rollquery', '')
        Domainquery = request.GET.get('Domainquery', '')
        Genderquery = request.GET.get('Genderquery', '')
        data = AuditionData.objects.all()

        if Namequery:
            data = data.filter(name__icontains=Namequery)
        elif Rollquery:
            data = data.filter(roll__icontains=Rollquery)
        elif Domainquery:
            data = data.filter(domain__icontains=Domainquery)
        elif Genderquery:
            data = data.filter(gender__icontains=Genderquery)

        # Filter works by query and type_of_work

        
        serializer = AuditionDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@csrf_exempt
def send_email_to_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_email = data.get('email')  # Extract email from the request
            
            if not user_email:
                return JsonResponse({'status': 'error', 'message': 'Email field is required.'})

            # Send success email to the user
            subject = "Welcome to SAE Audition - Let's Crush This Challenge! "
            message = "Congrats on moving forward to the SAE Audition! This is the college's most demanding audition, where only the best rise to the top. It's your chance to showcase your skills, creativity, and passion. \n \nPrepare to face exciting challenges that will push your limits and ignite your innovative spirit. Every task is an opportunity to shine and grow—whether it's teamwork, leadership, or technical expertise. \n \nWe know you're ready. Stay focused, bring your A-game, and make the most of every moment. \n \nLet's make this audition unforgettable. Best of luck!\n \n \n \nWarm regards, \nSAEINDIA Collegiate Club\nNIT Durgapur"
            from_email = 'saeindia@nitdgp.ac.in'  # Replace with your email
            recipient_list = [user_email]

            send_mail(subject, message, from_email, recipient_list)
            
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


class SendOtpView(APIView):
    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Delete any existing OTP for the given email
            OTP.objects.filter(email=email).delete()

            # Generate a new OTP
            otp = random.randint(100000, 999999)

            # Send OTP via email
            send_mail(
                'Your OTP for Admin Login',
                f'Your OTP is {otp}. Please use this OTP to log in to your admin account.',
                'saeindia@nitdgp.ac.in',  # Replace with your email
                [email],
                fail_silently=False,
            )

            # Save the new OTP to the database
            OTP.objects.create(otp=str(otp), email=email)

            return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class VerifyOtpView(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_input = serializer.validated_data['otp']

            try:
                otp_record = OTP.objects.get(email=email)

                # Check if OTP is expired
                if otp_record.is_expired():
                    return Response({"message": "OTP expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # Check if OTP matches
                if otp_record.otp == otp_input:
                    return Response({"success": True, "message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            except OTP.DoesNotExist:
                return Response({"message": "No OTP found for this email."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)