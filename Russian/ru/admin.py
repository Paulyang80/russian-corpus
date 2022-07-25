from django.contrib import admin

# Register your models here.
from .models import data_Russian, data_output

class YourModelAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "text",
    )
admin.site.register(data_Russian, YourModelAdmin)
admin.site.register(data_output)