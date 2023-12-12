from django.contrib import admin
from api.models import Entity

# Register your models here.
@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass
