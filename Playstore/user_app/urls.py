from django.urls import path
from . import views

urlpatterns = [
    
    
        #  .............. User Authentication..............
        
    path('Login/',views.Login,name='login'),
    
    path('Signup/',views.Signup,name='signup'),
    
    path('Signup_Otp/',views.Signup_Otp,name='signup_otp'),
    
    path('Logout/',views.Logout,name='logout'),
    
      #  ..............End User Authentication..............
    

      #  .............. Forget Password..............
      
    path('Forgot_pass/',views.Forgot_pass,name='forgot_pass'),
    
    path('New_pass/',views.New_pass,name='new_pass'),
    
    path('forget_OTP_check/',views.Forget_OTP_check,name='forget_OTP_check'),
    
       #  ..............End Forget Password..............

    
    
    path('Block_check/<int:id>',views.Block_Check,name='block_check'),
    
    path('resend_otp/',views.Signup_Resend_Otp,name='signup_resend_otp'), 
    
    path('forgot_resend_otp/',views.Forgot_Resend_Otp,name="forgot_resent_otp"),
    
    path('referral/',views.Referral,name="referral"),
    

 ]
