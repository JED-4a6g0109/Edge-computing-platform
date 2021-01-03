from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'file_upload', views.DocumentViewSet)



app_name = 'file_upload'
urlpatterns = [
    path('index/', views.filelist_view, name='file_list'),
    path('file_upload/', views.model_form_upload , name = 'upload'),
    path('edit/<int:pk>', views.file_update, name='file_edit'),
    path('delete/<int:pk>', views.file_delete, name='file_delete_model'),
    url(r'^api/', include(router.urls))


    # path('image/', views.image_upload_view),
    # path('update', views.fileupdate_view),

]
