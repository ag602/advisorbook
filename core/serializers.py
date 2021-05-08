from rest_framework import serializers
from .models import CustomUser, Advisor, Booking
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    name = serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomUser(email=self.validated_data['email'],
                          name=self.validated_data['name']
                          )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Password Mismatched'})
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        print(token)
        return token


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': False}
        }

    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            email = authenticate(request=self.context.get('request'),
                                email=username, password=password)
            if not email:
                msg = _("Credentials don't match!")
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['email'] = email
        print(data['email'])
        return data
    #
    # def create(self, validated_data):
    #     return CustomUser.objects.create(**validated_data)


class RegisterAdvisorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    photo_url = serializers.CharField(required=True)
    class Meta:
        model = Advisor
        fields = ['name', 'photo_url']

    def save(self):
        advisor = Advisor(name=self.validated_data['name'], photo_url=self.validated_data['photo_url'])
        advisor.save()
        return advisor

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'name',  'photo_url']


from django.utils import timezone
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user',  'advisor', 'booking_time']

    def save(self, *args, **kwargs):
        print(args, kwargs)
        booking = Booking(user=self.validated_data['user'],
                          advisor=self.validated_data['advisor'],
                          )
        print(booking)
        booking.save()
        return booking

class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user',  'advisor', 'booking_time']

    # def save(self):
    #     booking = Booking(user=self.validated_data['user'],
    #                       advisor=self.validated_data['advisor'],
    #                       )
    #     print(booking)
    #     booking.save()
    #     return booking


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'booking_time']
