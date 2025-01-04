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
def frontpage(request):
    return HttpResponse("This is backend")
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
        data = AuditionData.objects.all()

        if Namequery:
            data = data.filter(name__icontains=Namequery)
        elif Rollquery:
            data = data.filter(roll__icontains=Rollquery)
        elif Domainquery:
            data = data.filter(domain__icontains=Domainquery)

        # Filter works by query and type_of_work

        
        serializer = AuditionDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
