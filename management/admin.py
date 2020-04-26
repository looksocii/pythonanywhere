from django.contrib import admin
from webbrowser import register
from .models import *
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Permission) #สามารถเพิ่มสิทธิ์ได้

admin.site.register(Department)

admin.site.register(Manager)

admin.site.register(Employee)

admin.site.register(Company)

admin.site.register(Accountant)

admin.site.register(Sale)

admin.site.register(Store)

admin.site.register(Cost)

admin.site.register(Aperture)
