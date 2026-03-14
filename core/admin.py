from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Cabinet, Phase, File


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'cabinet', 'order', 'created_by')
    list_filter = ('cabinet',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_number', 'cabinet', 'status', 'is_deleted')
    list_filter = ('status', 'is_deleted', 'cabinet')
    search_fields = ('file_name', 'file_number')
