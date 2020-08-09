from django.urls import path, include
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static

appname = 'accounts'
urlpatterns = [
    path('', user_account_profile, name = 'profile'),
    path('dashboard/', user_dashboard, name = 'dashboard'),
    path('create/', user_create_profile, name = 'profile_create'),
    path('login/', user_login, name = 'user_login'),
    path('register/', user_register, name = 'user_register'),
    path('student/', create_and_auth_then_redirect, name = 'create_and_auth_then_redirect'),
    path('student/profile/', create_prof_then_redirect_to_another_then_log_out, name='create_prof_then_redirect_to_another_then_log_out'),
    path('logout/', user_logout, name = 'user_logout'),
    path('add_profile/', student_personal_info, name = 'student_personal_info'),
    path('referee_info/', referees_info, name = 'referees_info'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)