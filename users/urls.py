from django.urls import path
from .views import SignUp,CustomTokenObtainPairView, activate_account, resend_code
from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path('signup/', SignUp),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('activate/', activate_account, name='activate'),
    path('resend/', resend_code, name='resend_pin'),
    
]
