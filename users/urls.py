from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html',redirect_authenticated_user=True),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('register/',views.register,name='user-register'),
    path('profile/',views.profileDisplay,name='profile'),
    path('changePassword/', auth_views.PasswordChangeView.as_view(template_name='users/changePassword.html',), name='change-password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/changePasswordDone.html',), name='password_change_done')
]