from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('reservas/', reservasData, name='reservasData'),
    path('crear_reserva/', crear_reserva, name='crear_reserva'),
    path('eliminar_reserva/<int:id>', eliminar_reserva, name='eliminar_reserva'),
    path('editar_reserva/<int:id>', editar_reserva, name='editar_reserva'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('reservas_api/', ReservaListCreateView.as_view(), name='reservas_api'),
    path('reservas_api/<int:pk>/', ReservaDetailView.as_view(), name='reserva-detail'),
]