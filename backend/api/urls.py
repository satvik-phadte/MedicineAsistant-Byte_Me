# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register', views.register_user),
    path('auth/login', views.login_user),

    # Generic CRUD
    path('users/', views.users_list_create),
    path('users/<int:user_id>/', views.user_detail),

    path('pharmacies/', views.pharmacies_list_create),
    path('pharmacies/<int:pharmacy_id>/', views.pharmacy_detail),

    path('medicines/', views.medicines_list_create),
    path('medicines/<int:medicine_id>/', views.medicine_detail),
    path('medicines/search', views.search_medicine),

    # Prescriptions & OCR
    path('prescriptions/', views.prescriptions_list_create),
    path('prescriptions/<int:presc_id>/', views.prescription_detail),
    path('prescriptions/upload', views.upload_prescription),

    # Reminders
    path('reminders/', views.reminders_list_create),
    path('reminders/<int:reminder_id>/', views.reminder_detail),

    # Doctor prescriptions
    path('doctors/prescriptions', views.doctor_create_prescription),

    # Pharmacy inventory update
    path('pharmacies/inventory', views.pharmacy_update_inventory),
]
