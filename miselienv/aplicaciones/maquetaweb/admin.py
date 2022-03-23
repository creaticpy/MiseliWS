from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(SeccionesModel)
admin.site.register(SubSeccionesModel)
admin.site.register(SubSubSeccionesModel)
