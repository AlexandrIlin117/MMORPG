from django.contrib import admin
from .models import Publication,Category,Reaction


# Register your models here.
admin.site.register(Publication)
admin.site.register(Category)
admin.site.register(Reaction)