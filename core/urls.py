from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Cabinets
    path('cabinets/', views.cabinet_list, name='cabinet_list'),
    path('cabinets/create/', views.cabinet_create, name='cabinet_create'),
    path('cabinets/<int:pk>/', views.cabinet_detail, name='cabinet_detail'),
    path('cabinets/<int:pk>/edit/', views.cabinet_edit, name='cabinet_edit'),
    path('cabinets/<int:pk>/delete/', views.cabinet_delete, name='cabinet_delete'),

    # Phases
    path('cabinets/<int:cabinet_pk>/phases/create/', views.phase_create, name='phase_create'),
    path('phases/<int:pk>/delete/', views.phase_delete, name='phase_delete'),

    # Files
    path('files/', views.file_list, name='file_list'),
    path('files/create/', views.file_create, name='file_create'),
    path('files/<int:pk>/', views.file_detail, name='file_detail'),
    path('files/<int:pk>/edit/', views.file_edit, name='file_edit'),
    path('files/<int:pk>/delete/', views.file_delete, name='file_delete'),

    # Users (Admin)
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/toggle/', views.user_toggle_active, name='user_toggle_active'),

    # API
    path('api/file-number-suggestions/', views.api_file_number_suggestions, name='api_file_number_suggestions'),
    path('api/check-file-number/', views.api_check_file_number, name='api_check_file_number'),
    path('api/phases/', views.api_phases, name='api_phases'),
]
