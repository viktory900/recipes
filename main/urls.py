from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    path('main/', views.main_page, name='main_page'), 
    path('main/toggle-theme/', views.toggle_theme, name='toggle_theme'), 
    
    path('', views.form_view, name='form_view'),
    path('export/', views.export_to_xml, name='export_to_xml'),
    path('import/', views.import_from_xml, name='import_from_xml')
]
