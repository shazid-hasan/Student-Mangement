from django.shortcuts import redirect,render,HttpResponse
from django.contrib import messages
from myApp.models import customUser
from myApp import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def signupPage(request):
    error_messages = {
        'password_error': 'Password and Confirm Password not match',
    }

    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmpassword")

        if pass1!= pass2:
            messages.error(request, error_messages['password_error'])
        else:
            myuser = customUser.objects.create_user(username=uname, email=email, password=pass1)
            myuser.save()
            return redirect("loginPage")

    return render(request, "signup.html")

def loginPage(request):
    error_messages = {
        'username_error': 'Username is required.',
        'password_error': 'Password is required.',
        'login_error': 'Invalid username or password. Please try again.',
    }

    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")

        if not username:
            messages.error(request, error_messages['username_error'])
        elif not pass1:
            messages.error(request, error_messages['password_error'])
        else:
            user = EmailBackEnd.authenticate(request, username=username, password=pass1,)

            if user is not None:
                login(request,user)
                user_type = user.user_type
                if user_type == '1':
                    
                    return redirect("adminPage")

                elif user_type == '2':
                    return HttpResponse("Teacher")
                    
                elif user_type == '3':

                    return HttpResponse("students")
                
                else:
                    return redirect("signupPage")
            else:
                messages.error(request, error_messages['login_error'])

            
    return render(request, "login.html")

@login_required
def adminPage(request):
    return render(request, "myAdmin/adminPage.html")

def myProfile(request):

    user = request.user
    context = {
        'user': user
    }
    return render(request, "myProfile.html",context)

def updateProfile(request):
    error_messages = {
        'success': 'Profile Update Successfully',
        'error': 'Profile Not Updated',
        'password_error': 'Current password is incorrect',
    }


    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")


        try:
            cuser = customUser.objects.get(id=request.user.id)
            cuser.first_name = firstname
            cuser.last_name = lastname
            cuser.profile_pic = profile_pic

            if not cuser.check_password(password):
                messages.error(request, error_messages['password_error'])

            else:
                if profile_pic is not None:
                    cuser.profile_pic = profile_pic
                cuser.save()
                messages.success(request, error_messages['success'])
                return redirect("updateProfile")
        except:
            messages.error(request, error_messages['error'])

    return render(request, 'myProfile.html')


def logoutPage(request):
    logout(request)
    return redirect("loginPage")

def changePassword(request):

    error_messages = {
        'success': 'Changed Successfully',
        'mismatch': 'New password and confirm password not matched',
        'old_password': 'Old password not match',
    }

    if request.method == "POST":
        old_password = request.POST.get("oldPassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmPassword")
        user = request.user

        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()   
                messages.success(request, error_messages['success'])
                return redirect("loginPage")
            else:
                messages.error(request, error_messages['mismatch'])
        else:
            messages.error(request, error_messages['old_password'])

    return render(request, 'changePassword.html')
