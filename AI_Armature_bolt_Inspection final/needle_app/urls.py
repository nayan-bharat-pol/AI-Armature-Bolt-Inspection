# needle_app/urls.py
from django.urls import path
from . import views

app_name = 'needle_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('configuration/', views.configuration, name='configuration'),
     path('configuration/edit/', views.edit_configuration, name='edit_configuration'),
    path('initialization/', views.initialization, name='initialization'),
    path('run-inspection/', views.run_inspection, name='run_inspection'),
    path('end-inspection/', views.end_inspection, name='end_inspection'),
    path('inspection-status/', views.inspection_status, name='inspection_status'),
    path('get_needle_images/', views.get_needle_images, name='get_needle_images'),
    path("add-master-configuration/", views.add_master_configuration, name="add_master_configuration"),


    # auth
    path('custom-login/', views.custom_login, name='custom_login'),
    
         path('configuration/', views.configuration, name='configuration'),
]
  
  
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('needle_app.urls')),   # include app URLs
# ]