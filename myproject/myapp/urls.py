from django.urls import path
from .views import process_csv
from myapp.views import download_file, view_database
from myapp.views import delete_file

urlpatterns = [
    path('process_csv', process_csv, name='process_csv'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('view_database/', view_database, name='view_database'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
]