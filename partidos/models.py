from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True,
                                 null=True)  # Puedes usar un campo PointField si usas PostGIS
    rol_preferido = models.CharField(max_length=20, choices=[
        ('arquero', 'Arquero'),
        ('defensor', 'Defensor'),
        ('mediocampista', 'Mediocampista'),
        ('delantero', 'Delantero')
    ])
    nivel_habilidad = models.CharField(max_length=12, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    disponibilidad = models.TextField(blank=True, null=True)
    zona_horaria = models.CharField(max_length=50, choices=[(tz, tz) for tz in pytz.common_timezones])

    def __str__(self):
        return self.user.username


class Partido(models.Model):
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=255)  # Puedes usar un campo PointField si usas PostGIS
    fecha = models.DateField()
    hora = models.TimeField()
    nivel_habilidad = models.CharField(max_length=12, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    tipo_partido = models.CharField(max_length=20, choices=[
        ('amistoso', 'Amistoso'),
        ('competitivo', 'Competitivo'),
        # Agrega más opciones según tus necesidades
    ])
    jugadores_necesarios = models.PositiveIntegerField()

    def __str__(self):
        return f"Partido de {self.tipo_partido} - {self.fecha} {self.hora}"


class Participacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    equipo = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario} en {self.partido}"


class Calificacion(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='calificaciones_emitidas')
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='calificaciones_recibidas')
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    puntuacion = models.PositiveIntegerField()
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.emisor} calificó a {self.receptor} con {self.puntuacion} en {self.partido}"
