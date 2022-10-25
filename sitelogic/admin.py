from django.contrib import admin
from .models import Publication,Category,Reaction,OneTimeCode


# Register your models here.
admin.site.register(Publication)
admin.site.register(Category)
admin.site.register(Reaction)
admin.site.register(OneTimeCode)