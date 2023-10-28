from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + " " + self.user.username
    
class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='products/', null=True, blank=True)
    imagen1 = models.ImageField(upload_to='products/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}: {self.precio}"