from django.urls import path
from authapp import views     # To redirect to views of this app

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.handle_login, name='handle_login'),
    path('logout', views.handle_logout, name='handle_logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email', views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>/',views.SetNewPasswordView.as_view(), name='set-new-password'),

]
