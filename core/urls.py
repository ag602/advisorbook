from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    # path('', home_view, name='home'),
    # path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('admin/advisor/', AdvisorRegisterView.as_view(), name='advisor_register'),
    path('user/<slug:pk>/advisor', AdvisorListView.as_view(), name='advisor_list'),
    path('user/<int:pk1>/advisor/<int:pk2>', AdvisorBookView.as_view(), name='advisor_book'),
    path('user/<slug:users_id>/advisor/booking', BookedCallsView.as_view(), name='advisor_book_list'),
    path('user/register/', RegisterView.as_view(), name='register'),
 ]