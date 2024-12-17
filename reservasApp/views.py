from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from reservasApp.models import *
from reservasApp.forms import *
from reservasApp.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

# Create your views here.

class ReservaDetailView(APIView):
    """
    Vista para manejar el CRUD de una reserva específica (GET, PUT, PATCH, DELETE).
    """

    # Función para obtener una reserva específica
    def get_object(self, pk):
        try:
            return Reserva.objects.get(pk=pk)
        except Reserva.DoesNotExist:
            raise Http404

    # Obtener una reserva específica
    def get(self, request, pk):
        reserva = self.get_object(pk)
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data)

    # Actualizar completamente una reserva (PUT)
    def put(self, request, pk):
        reserva = self.get_object(pk)
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar parcialmente una reserva (PATCH)
    def patch(self, request, pk):
        reserva = self.get_object(pk)
        serializer = ReservaSerializer(reserva, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Eliminar una reserva
    def delete(self, request, pk):
        reserva = self.get_object(pk)
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservaListCreateView(APIView):
    """
    Vista para listar todas las reservas y crear una nueva.
    """

    # Listar todas las reservas
    def get(self, request):
        reservas = Reserva.objects.all()
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    # Crear una nueva reserva
    def post(self, request):
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def landing_page(request):
    return render(request, 'reservasApp/index.html')

def reservasData(request):
    reservas = Reserva.objects.all()
    data = {'reservas': reservas}
    return render(request, 'reservasApp/reservas.html', data)

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la reserva en la base de datos
            # Redirige a la vista de reservas
            return redirect('reservasData')  # Nombre de la vista que muestra las reservas
    else:
        form = ReservaForm()

    return render(request, 'reservasApp/crear_reserva.html', {'form': form})

def eliminar_reserva(request, id):
    #buscar reserva con su id
    reservas = Reserva.objects.get(id=id)
    reservas.delete()
    return HttpResponseRedirect(reverse('reservasData'))

def editar_reserva(request, id):
    reservas = Reserva.objects.get(id=id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reservas)
        if form.is_valid():
            form.save()  # Guarda la reserva en la base de datos
            # Redirige a la vista de reservas
            return redirect('reservasData')  # Nombre de la vista que muestra las reservas
    else:
        form = ReservaForm(instance=reservas)

    return render(request, 'reservasApp/crear_reserva.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')  # Redirigir al panel administrativo despues de iniciar sesion
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'reservasApp/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirigir al login tras registrarse

    return render(request, 'reservasApp/register.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')  # Redirige al index después de cerrar sesión

def admin_panel(request):
    return render(request, 'reservasApp/admin_panel.html')

