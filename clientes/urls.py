from django.urls import path
from .views import login, home, logout

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),  # Ruta para el logout
    path('home/', home, name="home" ),
]
