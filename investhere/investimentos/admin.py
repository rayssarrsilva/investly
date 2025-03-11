# Register your models here.

from django.contrib import admin 
from .models import Investimento

admin.site.register(Investimento) #Agora os investimentos poderão ser gerenciados no painel administrativo.
