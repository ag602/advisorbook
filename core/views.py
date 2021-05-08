from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from .models import CustomUser, Advisor
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import update_last_login
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer, RegisterAdvisorSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers

# Create your views here.
import requests

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializers

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                response = {
                    "user_id": user.id,
                    "token": get_tokens_for_user(user)
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not email or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AdvisorRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Advisor.objects.all()
    serializer_class = RegisterAdvisorSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        c = Advisor.objects.create(name=data.get('name'), photo_url=data.get('photo_url'))
        return Response ({"name":data.get('name'), "photo_url":data.get('photo_url'), "id":c.id})

from django.http import JsonResponse

class AdvisorListView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        advisor_set = Advisor.objects.all().values()
        # print(advisor_set[0]['advisor'])
        return Response(advisor_set, status=status.HTTP_200_OK )

import json
class AdvisorBookView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def post(self, *args, **kwargs):
        pk_user = kwargs.get('pk1', None)
        pk_advisor = kwargs.get('pk2', None)
        booking = Booking.objects.create(user_id=pk_user, advisor_id=pk_advisor)
        data = {"Booking id": booking.id, "User": booking.user.name, "Advisor": booking.advisor.name,
                "Booking Time": booking.booking_time}
        return Response(data, status=status.HTTP_201_CREATED)

class BookedCallsView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BookingListSerializer

    def get(self, request, *args, **kwargs):
        files = Booking.objects.filter(user=kwargs.get('users_id')).values()
        data = []

        for item in files:
            # print(item)
            dic = {}
            advisor = Advisor.objects.get(id=item['advisor_id'])
            dic['Advisor Name'] = advisor.name
            dic['Profile Pic'] = advisor.photo_url
            dic['Advisor Id'] = advisor.id
            dic['Booking Time'] = item['booking_time']
            dic['Booking Id'] = item['id']
            print(dic)
            data.append(dic)
        return Response(data, status=status.HTTP_200_OK )

    def get_queryset(self):
        return None
