from django.urls import path
from . import views

app_name = 'farm'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('crops/', views.crop_list_view, name='crop_list'),
    path('crops/add/', views.crop_create_view, name='crop_create'),
    path('crops/<int:pk>/', views.crop_detail_view, name='crop_detail'),
    path('crops/<int:pk>/edit/', views.crop_update_view, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete_view, name='crop_delete'),
    path('crops/<int:crop_pk>/expenses/add/', views.expense_create_view, name='expense_create'),
    path('crops/<int:crop_pk>/sales/add/', views.sale_create_view, name='sale_create'),
]