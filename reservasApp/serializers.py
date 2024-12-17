from rest_framework import serializers
from reservasApp.models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'  # Incluir todos los campos del modelo