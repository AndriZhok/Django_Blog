from django.urls import path, include

from users import views

app_name = 'users'

urlpatterns = [
    # Додати уставні URL для автентифікації
    path('', include('django.contrib.auth.urls')),
    # Сторінка реєстрації.
    path('register/', views.register, name='register'),
]