



from django.urls import path
from. import views
urlpatterns = [
  
  path('signup/', views.UserSignupView.as_view(), name='user_signup'),
  path('login/', views.User_login.as_view(), name='login'),
  path('logout/',views.Logout.as_view(),name='logout'),
  path('varifi_otp/', views.Varifi_otp_.as_view(), name='varifi_otp'),
  
 # path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
 #path('requestpasswordreset/', views.RequestPasswordReset.as_view(), name='RequestPasswordReset'),
 # path('reset-password/<str:token>/', views.ResetPassword.as_view(), name='password-reset'),
  
]