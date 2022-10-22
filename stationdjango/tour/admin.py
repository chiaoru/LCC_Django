from django.contrib import admin

# Register your models here.


from .models import Tour


class tourAdmin(admin.ModelAdmin):
    list_display = ('title','price','create_date')

admin.site.register(Tour,tourAdmin)

