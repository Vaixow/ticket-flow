from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    class Categoria(models.TextChoices):
        SOPORTE = "soporte", "Soporte"
        BUG = "bug", "Bug"
        MEJORA = "mejora", "Mejora"

    class Prioridad(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"

    class Estado(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        EN_PROCESO = "en_proceso", "En Proceso"
        RESUELTO = "resuelto", "Resuelto"

    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=Categoria.choices, default=Categoria.SOPORTE)
    prioridad = models.CharField(max_length=20, choices=Prioridad.choices, default=Prioridad.MEDIA)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NUEVO)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} {self.titulo}"
