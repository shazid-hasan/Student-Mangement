
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.signupPage,name="signupPage"),
    path('loginPage',views.loginPage,name="loginPage"),
    path('adminPage',views.adminPage,name="adminPage"),
    path('myProfile',views.myProfile,name="myProfile"),
     path('profile/updateProfile', views.updateProfile,name="updateProfile"), 
     path('loginPage', views.logoutPage,name="logoutPage"), 
     path('profile/changePassword', views.changePassword,name="changePassword"), 
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
