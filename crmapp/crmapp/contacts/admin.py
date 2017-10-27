from django.contrib import admin

from .models import Contact
# Register your models here.
admin.site.register(Contact,
                    list_display = ['first_name','last_name','uuid'],
                    readonly_fields = ['uuid'])
