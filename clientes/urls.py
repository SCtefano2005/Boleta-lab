from django.urls import path
from .views import login, factura_view, logout

urlpatterns = [
    path('logout/', logout, name='logout'),  
    path('factura/<int:factura_id>/', factura_view, name='factura_view'),
]
