from django.db import models

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('reservado', 'Reservado'),
        ('completada', 'Completada'),
        ('anulada', 'Anulada'),
        ('no_asisten', 'No Asisten'),
    ]

    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    fecha = models.DateField()  # Fecha específica
    hora = models.TimeField()  # Hora específica
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='reservado')  # Opciones limitadas
    personas = models.PositiveSmallIntegerField(default=1)  # Número de personas entre 1 y 15
    observacion = models.TextField(blank=True, null=True)  # Campo opcional

    def save(self, *args, **kwargs):
        # Validación personalizada para el número de personas
        if self.personas < 1 or self.personas > 15:
            raise ValueError("El número de personas debe estar entre 1 y 15.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.nombre} el {self.fecha} a las {self.hora} para {self.personas} personas. Estado: {self.estado}"