from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re

#for token and 100%authentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from authapp.utils import TokenGenerator, generate_token

#For email veification stuffs
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings


#For email sending
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.conf import settings
from django.core import mail


def signup(request):
    flag=0
    if request.method == "POST": 
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        print(name,email,password,confirm_password)

        if password != confirm_password:
            messages.warning(request, "Password is Not Matching")
            return redirect('/auth/signup')
        if len(password) <= 5:
            messages.warning(request, "Password must be atleast 5 character")
            return redirect('/auth/signup')
        elif not re.search("[a-z]", password):
            flag = -1

        elif not re.search("[A-Z]", password):
            flag = -1

        elif not re.search("[0-9]", password):
            flag = -1

        elif not re.search("[_@$#%^*()-]", password):
            flag = -1
        else:
            pass
        if (flag == 0):
            try:
                if User.objects.get(username=email):
                    # return HttpResponse("email already exist")
                    messages.info(request, "Email already a user")
                    return redirect('/auth/signup')

            except Exception as identifier:
                pass
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.is_active = False
            user.save()


            #Email verification stuufs
            
            email_subject = "Activate Your Account"
            message = render_to_string('activate.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)

            })


            #Email stuffs


            from_email = settings.EMAIL_HOST_USER
            connection = mail.get_connection()
            connection.open()
            #email_message = mail.EmailMessage(f'Email from {name}',
             #                             f'UserEmail : {email}',
             #                             from_email, [
             #                                '61bijilkv74@gmail.com'],
              #                            connection=connection)
            email_client = mail.EmailMessage(
                'N-Y-T Email verification', f"Activate Your Account by clicking the link {message}\n\nNi-Yan-Tron\n9497448320\n321bijil123@gmail.com", from_email, [email], connection=connection)

            connection.send_messages([ email_client])
            connection.close()


            messages.success(
               request, f"Activate Your Account by clicking the link in your gmail {email}")

            
            return redirect('/auth/login')
        

        else:
            messages.error(request, "Password is not valid")
            return redirect('/auth/signup')

    return render(request, "signup.html")








def handle_login(request):

    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request, myuser)
            #messages.success(request, "Login Success")
            return redirect('/')

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')

    return render(request, "login.html")


def handle_logout(request):
    logout(request)
    #messages.success(request, "Logout success")
    return render(request,"login.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('/auth/login')
        return render(request, 'activatefail.html')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'request-reset-email.html')

    def post(self, request):

        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject = '[Reset Your Password]'
            message = render_to_string('reset-user-password.html', {
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            })


            from_email = settings.EMAIL_HOST_USER
            connection = mail.get_connection()
            connection.open()
            # email_message = mail.EmailMessage(f'Email from {name}',
            #                             f'UserEmail : {email}',
            #                             from_email, [
            #                                '61bijilkv74@gmail.com'],
            #                            connection=connection)
            email_client = mail.EmailMessage(
                'N-Y-T Password reset request', f"---Reset Your Account Password --- {message}\n\nNi-Yan-Tron\n9497448320\n321bijil123@gmail.com", from_email, [email], connection=connection)

            connection.send_messages([email_client])
            connection.close()

            messages.success(
                request, f"Reset Your Account password by clicking the link in your mail {email}")

            return render(request, 'request-reset-email.html')












            # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            # email_message.send()

           # messages.info(request, f"{message} ")
            #return render(request, 'request-reset-email.html')
        else:
            messages.error(request, 'No Account Exists with this email')
            return render(request, 'request-reset-email.html')


class SetNewPasswordView(View):

    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password Reset Link is Invalid")
                return render(request, 'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request, 'set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        flag = 0
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is Not Matching")
            return render(request, 'set-new-password.html', context)

        if len(password) <= 8:
            messages.warning(request, "Password must be atleast 8 character")
            return render(request, 'set-new-password.html', context)
        elif not re.search("[a-z]", password):
            flag = -1

        elif not re.search("[A-Z]", password):
            flag = -1

        elif not re.search("[0-9]", password):
            flag = -1

        elif not re.search("[_@$#]", password):
            flag = -1
        else:
            pass

        if (flag == 0):
            try:
                user_id = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=user_id)
                user.set_password(password)
                user.save()
                messages.success(
                    request, "Password Reset Success Please Login with NewPassword")
                return redirect('/')

            except DjangoUnicodeDecodeError as identifier:
                messages.error(request, "Something Went Wrong")
                return render(request, 'set-new-password.html', context)
            else:
                messages.error(request, "Password is not valid")
                return redirect('/auth/signup')
