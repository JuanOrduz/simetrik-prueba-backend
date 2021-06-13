from django.urls import path

from csv_manager import views

urlpatterns = [
    path("", views.CSVFilesListCreate.as_view(), name="csv-files-list-create"),
    path(
        "<int:pk>/",
        views.CSVFilesRetrieveUpdateDestroyView.as_view(),
        name="csv-files-retrieve-update-destroy",
    ),
]
