from django.contrib import admin
from .models import User, Address, Format, Tournament

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display="first_name","last_name","email","password","administrator"

class AddressAdmin(admin.ModelAdmin):
    list_display="municipality","state","neighborhood","street","number","cep","user"

class FormatAdmin(admin.ModelAdmin):
    display="format_name"

class TournamentAdmin(admin.ModelAdmin):
    list_display="name","quantity_participants","format","user"

admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Format, FormatAdmin)
admin.site.register(Tournament, TournamentAdmin)