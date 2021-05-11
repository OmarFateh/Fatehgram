from django.urls import path

from .views import (
    user_register,
    validate_username, 
    validate_email,
    user_login, 
    user_logout,
)

urlpatterns = [
    # Authentication
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # js validations
    path('ajax/username/validate/', validate_username, name='js-validate-username'),
    path('ajax/email/validate/', validate_email, name='js-validate-email'),
]    