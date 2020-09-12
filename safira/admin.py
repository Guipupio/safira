from django.contrib import admin

from .models import Transacao, Cliente

admin.site.register(Transacao)
admin.site.register(Cliente)